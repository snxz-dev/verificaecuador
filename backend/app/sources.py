"""Fuentes reales de fact-checking (en vivo, sin API key).

Cuando la base de datos no tiene una verificación, se consultan en orden:
1. Ecuador Chequea (API REST WordPress)
2. Google Fact Check Tools (agrega verificaciones de muchas organizaciones)
3. Primera Plana (API REST WordPress, solo artículos estilo fact-check)
4. RSS de Ecuador Chequea (fallback con lo más reciente)

Cada fuente es opcional: si una falla, las demás siguen funcionando.
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
from xml.etree import ElementTree

import httpx

logger = logging.getLogger(__name__)

TIMEOUT = 8.0
# UA de navegador: varias APIs públicas rechazan clientes no-navegador (406)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

ECUADOR_CHEQUEA_API = "https://www.ecuadorchequea.com/wp-json/wp/v2/posts"
ECUADOR_CHEQUEA_FEED = "https://ecuadorchequea.com/feed/"
PRIMERA_PLANA_API = "https://primeraplana.com.ec/wp-json/wp/v2/posts"
GOOGLE_FACTCHECK_API = "https://toolbox.google.com/factcheck/api/search"

# Categoría "Verificaciones" de Ecuador Chequea: solo artículos de fact-checking
ECUADOR_CHEQUEA_CATEGORY_VERIFICACIONES = 4289

# Patrones de veredicto que los fact-checkers usan al inicio del título
VERDICT_PATTERNS = [
    re.compile(r"^(Es\s+(falso|falsa|cierto|cierta|engañoso|engañosa|verdadero|verdadera)\s+(que|decir|afirmar|que\s+[a-záéíóúñ]))"),
    re.compile(r"^(Falso|Falsa|Cierto|Cierta|Engañoso|Engañosa|Verdadero|Verdadera|Real|Mentira|Verdad)\b"),
]


def _extract_verdict(title: str) -> str:
    """Extrae el veredicto de la primera parte del título."""
    for pat in VERDICT_PATTERNS:
        m = pat.search(title)
        if m:
            return m.group(1).capitalize()
    return "Verificación"


def _looks_like_factcheck(title: str) -> bool:
    """True si el título parece un artículo de fact-checking."""
    return any(pat.search(title) for pat in VERDICT_PATTERNS)


def _clean_html(html: str, max_len: int = 400) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def _query_words(query: str, max_words: int = 6) -> list:
    return [w for w in query.lower().split() if len(w) > 3][:max_words]


def _to_wp_match(post: dict, source: str) -> dict:
    """Convierte un post de WordPress al formato que usa el bot y la web."""
    title = post["title"]["rendered"]
    media = post.get("_embedded", {}).get("wp:featuredmedia") or []
    image = media[0].get("source_url", "") if media else ""
    return {
        "claim": title,
        "verdict": _extract_verdict(title),
        "source": source,
        "url": post["link"],
        "explanation": _clean_html(post.get("content", {}).get("rendered", "")),
        "image": image,
        "theme": "",
        "date": post.get("date", ""),
        "live": True,
    }


def _first_image(html: str) -> str:
    """Extrae la primera URL de imagen de un HTML."""
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html or "")
    return m.group(1) if m else ""


async def _search_wordpress(api_url: str, query: str, source: str, limit: int,
                            only_factchecks: bool = False, categories: int | None = None) -> list:
    """Busca en una API REST de WordPress por palabras clave (con 1 reintento)."""
    words = _query_words(query)
    if not words:
        return []
    params = {
        "search": " ".join(words),
        "per_page": limit,
        # _embed trae la imagen destacada; _fields la cortaría, así que no se usa
        "_embed": "",
    }
    if categories:
        params["categories"] = categories

    posts = None
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
                resp = await client.get(api_url, params=params, headers={"User-Agent": USER_AGENT})
                resp.raise_for_status()
                posts = resp.json()
            break
        except Exception as e:
            logger.warning("%s API falló (intento %d): %r", source, attempt + 1, e)
            if attempt == 0:
                await asyncio.sleep(0.6)
    if posts is None:
        return []

    results = []
    for p in posts or []:
        title = p["title"]["rendered"]
        if only_factchecks and not _looks_like_factcheck(title):
            continue
        results.append(_to_wp_match(p, source))
    return results


async def _search_google_factcheck(query: str, limit: int) -> list:
    """Busca en Google Fact Check Tools (sin API key).

    El endpoint público devuelve un JSON con prefijo de protección ()]}').
    Estructura: data[0][1] = lista de claims; cada claim[0] es un array con
    [0]=texto, [3]=lista de reviews con [0]=editorial, [1]=url, [2]=fecha,
    [3]=veredicto, [8]=título de la review.
    """
    words = _query_words(query)
    if not words:
        return []
    params = {"query": " ".join(words), "hl": "es"}
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(GOOGLE_FACTCHECK_API, params=params,
                                    headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            raw = resp.text
            if raw.startswith(")]}'"):
                raw = raw[4:].lstrip()
            data = json.loads(raw)
    except Exception as e:
        logger.warning("Google Fact Check falló: %s", e)
        return []

    results = []
    try:
        claims = data[0][1] or []
        for entry in claims:
            if len(results) >= limit:
                break
            try:
                claim_data = entry[0]
                text = claim_data[0]
                reviews = claim_data[3] or []
                if not text or not reviews:
                    continue
                review = reviews[0]
                publisher = (review[0][0] if review[0] else None) or "Google Fact Check"
                url = review[1] or ""
                rating = review[3] or "Verificación"
                review_title = review[8] or ""
                ts = review[2] or 0
                image = entry[1] if len(entry) > 1 and isinstance(entry[1], str) else ""
                results.append({
                    "claim": text,
                    "verdict": str(rating).capitalize(),
                    "source": publisher,
                    "url": url,
                    "explanation": review_title,
                    "image": image,
                    "theme": "",
                    "date": datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else "",
                    "live": True,
                })
            except Exception:
                continue
    except Exception as e:
        logger.warning("Parseo de Google Fact Check falló: %s", e)
    return results


async def _search_rss(feed_url: str, query: str, source: str, limit: int) -> list:
    """Busca por palabras clave en un feed RSS."""
    words = _query_words(query)
    if not words:
        return []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(feed_url, headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            root = ElementTree.fromstring(resp.content)
    except Exception as e:
        logger.warning("RSS %s falló: %s", source, e)
        return []

    content_ns = "{http://purl.org/rss/1.0/modules/content/}"
    results = []
    for item in root.iter("item"):
        if len(results) >= limit:
            break
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        content_html = item.findtext(content_ns + "encoded") or item.findtext("description") or ""
        desc = _clean_html(content_html, 300)
        haystack = f"{title} {desc}".lower()
        if not any(w in haystack for w in words):
            continue
        if not _looks_like_factcheck(title):
            continue
        results.append({
            "claim": title,
            "verdict": _extract_verdict(title),
            "source": source,
            "url": link,
            "explanation": desc,
            "image": _first_image(content_html),
            "theme": "",
            "date": item.findtext("pubDate") or "",
            "live": True,
        })
    return results


async def search_live_sources(query: str, limit: int = 5) -> list:
    """Busca verificaciones en vivo en varias fuentes, sin duplicados."""
    tasks = [
        _search_wordpress(ECUADOR_CHEQUEA_API, query, "Ecuador Chequea", limit,
                          categories=ECUADOR_CHEQUEA_CATEGORY_VERIFICACIONES),
        _search_google_factcheck(query, limit),
        _search_wordpress(PRIMERA_PLANA_API, query, "Primera Plana", limit,
                          only_factchecks=True),
        _search_rss(ECUADOR_CHEQUEA_FEED, query, "Ecuador Chequea (RSS)", max(2, limit // 2)),
    ]

    all_results = []
    for task in tasks:
        try:
            all_results.extend(await task)
        except Exception as e:
            logger.warning("Fuente en vivo falló: %s", e)

    seen = set()
    unique = []
    for m in all_results:
        key = m["url"].rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        unique.append(m)

    logger.info("Fuentes en vivo: %d resultados para %r", len(unique), query)
    return unique[: limit * 2]

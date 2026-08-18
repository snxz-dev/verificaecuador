"""Punto de entrada: API web + bot de Telegram."""

import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db import SessionLocal, search_fact_checks
from .detector import classify
from .sources import search_live_sources

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="VerificaEcuador API", version="0.1.0")

# La web (Astro) llama a la API desde el navegador; CORS abierto para la demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"app": "VerificaEcuador", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/verify")
async def verify(body: dict):
    """Endpoint para verificar un texto (lo usa la app Flutter)."""
    text = body.get("text", "").strip()
    if not text:
        return JSONResponse({"error": "texto vacío"}, status_code=400)

    classification = classify(text)
    db = SessionLocal()
    try:
        matches = search_fact_checks(db, text)
    finally:
        db.close()

    live = await search_live_sources(text)
    seen = {m["url"] for m in matches}
    matches += [m for m in live if m["url"] not in seen]

    return {"classification": classification, "matches": matches, "live_sources": True}


async def startup() -> None:
    # El bot de Telegram corre en su propio servicio (docker-compose: bot).
    # Aquí solo queda la API web.
    from .config import TELEGRAM_TOKEN

    if not TELEGRAM_TOKEN:
        logger.warning("TELEGRAM_TOKEN no configurado: el bot no arranca. Solo API disponible.")


@app.on_event("startup")
async def on_startup() -> None:
    await startup()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

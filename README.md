# VerificaEcuador

Prototipo para **MediaHack II** (Openlab Ecuador + KAS, 14-15 ago 2026): herramienta
contra la **desinformación electoral** en Ecuador (elecciones 29 nov 2026).

Ciudadanos envían una afirmación/noticia por **Telegram** y reciben:
- Nivel de riesgo de desinformación (alto / moderado / sin señales).
- Verificaciones existentes con fuente (CNE, Ecuador Chequea, Primera Plana) y URL.
- Un aviso de que ninguna respuesta es un juicio: siempre se remite a la fuente original.

## Stack

| Capa | Tecnología |
|---|---|
| Bot | Python + python-telegram-bot (long polling) |
| API web | FastAPI (endpoint `/verify`) |
| Web | Astro (estático): página de verificación en `frontend/` |
| Base de datos | PostgreSQL serverless en la nube (Neon) |
| Detección | Reglas lingüísticas + señales (sin IA, sin dependencias externas) |
| Orquestación | Docker Compose (backend + bot + frontend) |

El backend y el bot corren en Docker; la base de datos vive en **Neon** (Postgres serverless).

## Cómo correr

```bash
cp .env.example .env   # pega tu TELEGRAM_TOKEN, tu DATABASE_URL de Neon y PUBLIC_API_URL
docker compose up -d   # levanta backend + bot + frontend
```

- API: http://localhost:8000
- Web: http://localhost:4321
- Bot: habla con tu bot en Telegram.

La web llama a la API desde el navegador (CORS abierto para la demo). Si la API
está en otra URL (p. ej. al desplegar), cambia `PUBLIC_API_URL` en `.env` y
reconstruye el frontend (`docker compose build frontend`).

> **Primera vez:** la tabla `fact_checks` no se crea sola. Ejecuta `db/seed.sql`
> una sola vez desde el SQL editor de Neon (o con `psql -f db/seed.sql "$DATABASE_URL"`).

## Despliegue (propuesta de demo con URL pública)

| Pieza | Dónde | Cómo |
|---|---|---|
| **Web (Astro)** | Vercel | Importa el repo, framework Astro (auto-detectado). Env var `PUBLIC_API_URL` = URL de la API. |
| **API (FastAPI)** | Render | `render.yaml` incluido: blueprint con web service + worker del bot. Env vars `DATABASE_URL` (Neon) y `TELEGRAM_TOKEN`. |
| **Base de datos** | Neon | Ya está en la nube: funciona desde cualquier host sin cambios. |

Pasos:
1. Commit + push a GitHub (`github.com/snxz-dev/verificaecuador`).
2. **Render:** New → Blueprint → selecciona el repo (usa `render.yaml`). Llena las env vars.
3. **Vercel:** New Project → importa el repo → framework **Astro** → env var
   `PUBLIC_API_URL=https://<tu-api>.onrender.com` → Deploy.
4. La web queda en `https://<proyecto>.vercel.app`; CORS ya está abierto (`*`).

> El bot de Telegram (long polling) corre como *worker* en Render; también puede
> quedarse solo en local para la demo si no se quiere otro servicio.

## Probar la API

```bash
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"text":"se anularon las elecciones de noviembre urgente"}'
```

## Cómo funciona la detección

`backend/app/detector.py` combina:
1. **Señales de riesgo** (palabras típicas de desinformación: "urgente", "confirmado",
   "se anularon", "en cadena", etc.).
2. **Temas electorales** (elecciones, CNE, padrón, fraude, bono, debate...).
3. **Base de verificaciones**: búsqueda por palabras clave en `fact_checks` (seed en `db/seed.sql`).

No emite juicios editoriales: solo clasifica riesgo y enlaza fuentes verificadas.

## Marco ético (condición de participación)

- Supervisión humana: no hay veredictos automáticos, se remite a fuentes.
- Neutralidad política: no favorece ni perjudica candidaturas.
- Protección de datos: no se almacenan mensajes de usuarios.
- Código abierto.

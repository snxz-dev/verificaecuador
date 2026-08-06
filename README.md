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
| API web | FastAPI (endpoint `/verify` para futura app móvil) |
| Base de datos | PostgreSQL 16 (Docker) |
| Detección | Reglas lingüísticas + señales (sin IA, sin dependencias externas) |
| Orquestación | Docker Compose |

Todo corre en Docker: no se instala nada en el sistema.

## Cómo correr

```bash
cp .env.example .env   # pega tu TELEGRAM_TOKEN
docker compose up -d   # levanta db + backend + bot
```

- API: http://localhost:8000
- Bot: habla con tu bot en Telegram.

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

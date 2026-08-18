"""Bot de Telegram: recibe mensajes, clasifica y responde con fuentes verificadas."""

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .config import TELEGRAM_TOKEN
from .db import SessionLocal, search_fact_checks
from .detector import classify
from .sources import search_live_sources

logger = logging.getLogger(__name__)


def format_response(classification: dict, matches: list) -> str:
    lines = []
    lines.append(f"🔎 {classification['risk_label']}")

    if classification["signals"]:
        lines.append("")
        lines.append("Señales detectadas: " + ", ".join(f'"{s}"' for s in classification["signals"]))

    if classification["themes"]:
        lines.append("Temas: " + ", ".join(classification["themes"]))

    lines.append("")
    if matches:
        lines.append("📌 **Verificaciones encontradas:**")
        for m in matches:
            lines.append(f"• {m['claim']}")
            lines.append(f"  → {m['verdict']} · {m['source']}")
            lines.append(f"  {m['url']}")
    else:
        lines.append(
            "No encontramos una verificación previa para este contenido. "
            "Te recomendamos contrastarlo con fuentes oficiales "
            "(CNE, Ecuador Chequea, Primera Plana)."
        )

    lines.append("")
    lines.append("_VerificaEcuador no emite juicios: siempre consulta la fuente original._")
    return "\n".join(lines)


async def start(update: Update, _ctx) -> None:
    await update.message.reply_text(
        "👋 Hola, soy **VerificaEcuador**.\n\n"
        "Mándame un texto, una afirmación o una noticia y te ayudo a "
        "verificarla contra fuentes confiables.\n\n"
        "Ej: *\"se anularon las elecciones de noviembre\"*"
    )


async def handle_message(update: Update, _ctx) -> None:
    if not update.message or not update.message.text:
        await update.message.reply_text("Solo puedo analizar texto por ahora.")
        return

    text = update.message.text.strip()
    if len(text) > 2000:
        text = text[:2000]

    classification = classify(text)
    db = SessionLocal()
    try:
        matches = search_fact_checks(db, text)
    finally:
        db.close()

    live = await search_live_sources(text)
    seen = {m["url"] for m in matches}
    matches += [m for m in live if m["url"] not in seen]

    response = format_response(classification, matches)
    await update.message.reply_text(response, parse_mode="Markdown")


def run_bot() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot VerificaEcuador iniciado (long polling)")
    # stop_signals vacío: corre sin signal handlers (proceso contenedor)
    app.run_polling(stop_signals=())


if __name__ == "__main__":
    run_bot()

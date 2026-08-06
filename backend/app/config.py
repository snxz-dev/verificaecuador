import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://verifica:verifica@localhost:5432/verificaecuador")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def search_fact_checks(db, query: str, limit: int = 5):
    """Busca verificaciones por palabras clave en el claim o tema."""
    words = [w for w in query.lower().split() if len(w) > 3]
    if not words:
        return []
    conditions = " OR ".join(
        "claim ILIKE :p%d OR theme ILIKE :p%d OR keywords ILIKE :p%d" % (i, i, i)
        for i in range(len(words))
    )
    params = {"p%d" % i: f"%{w}%" for i, w in enumerate(words)}
    sql = (
        "SELECT id, claim, verdict, source, url, explanation, theme "
        "FROM fact_checks WHERE %s ORDER BY created_at DESC LIMIT :limit"
        % conditions
    )
    rows = db.execute(text(sql), {**params, "limit": limit}).mappings().all()
    return [dict(r) for r in rows]

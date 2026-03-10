"""Database connection and session management."""

import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DEFAULT_DATABASE_URL = (
    "postgresql+psycopg2://healthuser:hM5Z.C6fU2G-FqCt@127.0.0.1:5432/health"
)


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def get_database_url():
    """Resolve the database URL from DATABASE_URL or PostgreSQL env vars."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    pg_env_keys = {"PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"}
    if any(os.getenv(key) for key in pg_env_keys):
        return URL.create(
            "postgresql+psycopg2",
            username=os.getenv("PGUSER", "healthuser"),
            password=os.getenv("PGPASSWORD", "hM5Z.C6fU2G-FqCt"),
            host=os.getenv("PGHOST", "127.0.0.1"),
            port=int(os.getenv("PGPORT", "5432")),
            database=os.getenv("PGDATABASE", "health"),
        ).render_as_string(hide_password=False)

    return DEFAULT_DATABASE_URL


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_url(), echo=False, pool_pre_ping=True)
    return _engine


def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return _SessionLocal()


def init_db():
    """Create all tables if they don't exist."""
    from johnny import models  # noqa: F401 – registers models with Base
    Base.metadata.create_all(get_engine())

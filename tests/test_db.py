"""Tests for database URL resolution."""

from johnny import db


def test_get_database_url_uses_default_postgres_credentials(monkeypatch):
    for key in ("DATABASE_URL", "PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"):
        monkeypatch.delenv(key, raising=False)

    assert (
        db.get_database_url()
        == "postgresql+psycopg2://healthuser:hM5Z.C6fU2G-FqCt@127.0.0.1:5432/health"
    )


def test_get_database_url_prefers_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://user:pass@db:5432/custom")
    monkeypatch.setenv("PGHOST", "ignored-host")

    assert db.get_database_url() == "postgresql+psycopg2://user:pass@db:5432/custom"


def test_get_database_url_builds_from_pg_env(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("PGHOST", "db.internal")
    monkeypatch.setenv("PGPORT", "5433")
    monkeypatch.setenv("PGUSER", "runner")
    monkeypatch.setenv("PGPASSWORD", "secret")
    monkeypatch.setenv("PGDATABASE", "metrics")

    assert db.get_database_url() == "postgresql+psycopg2://runner:secret@db.internal:5433/metrics"

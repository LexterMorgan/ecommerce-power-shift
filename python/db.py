"""PostgreSQL connection helpers for analytical layer (Gate 7B+). Not used by the public static dashboard."""
from __future__ import annotations

import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

DEFAULT_DATABASE_URL = "postgresql+psycopg://localhost:5432/ecommerce_power_shift"


def database_url() -> str:
    raw = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL).strip()
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw[len("postgres://") :]
    if raw.startswith("postgresql://") and "+psycopg" not in raw and "+psycopg2" not in raw:
        raw = "postgresql+psycopg://" + raw[len("postgresql://") :]
    return raw


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(database_url(), future=True, pool_pre_ping=True)

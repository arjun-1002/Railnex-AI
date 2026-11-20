"""
RailRakshak AI — Database Session Management
Provides SQLAlchemy Engine and SessionLocal with SQLite support.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, "railrakshak.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency injection helper for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

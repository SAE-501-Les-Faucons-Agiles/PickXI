from pathlib import Path
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DB_FOLDER = Path(__file__).resolve().parent
DB_FILE = DB_FOLDER / "football_reco.db"

# Configuration SQLAlchemy ORM
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, echo=False)
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
ScopedSession = scoped_session(SessionFactory)


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_session():
    """Retourne une session SQLAlchemy thread-safe"""
    return ScopedSession()


def init_db():
    connection = get_connection()
    try:
        schema = (DB_FOLDER / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()

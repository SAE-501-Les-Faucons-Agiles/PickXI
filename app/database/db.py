
from pathlib import Path
import sqlite3

DB_FOLDER = Path(__file__).resolve().parent
DB_FILE = DB_FOLDER / "football_reco.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    connection = get_connection()
    try:
        schema = (DB_FOLDER / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()

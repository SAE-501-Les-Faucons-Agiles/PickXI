import os
import csv
import sqlite3
import click
from typing import Optional
from flask import g, current_app, Flask
from app.config import Config

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id INTEGER,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    overall INTEGER NOT NULL,
    position TEXT NOT NULL,
    positions TEXT NOT NULL,
    club TEXT NOT NULL,
    league TEXT NOT NULL,
    nationality TEXT NOT NULL,
    price INTEGER NOT NULL,
    pace INTEGER NOT NULL,
    shooting INTEGER NOT NULL,
    passing INTEGER NOT NULL,
    dribbling INTEGER NOT NULL,
    defending INTEGER NOT NULL,
    physic INTEGER NOT NULL,
    weak_foot INTEGER NOT NULL,
    skill_moves INTEGER NOT NULL,
    image_url TEXT
);

CREATE INDEX IF NOT EXISTS idx_players_overall ON players(overall DESC);
CREATE INDEX IF NOT EXISTS idx_players_position ON players(position);
CREATE INDEX IF NOT EXISTS idx_players_price ON players(price);
CREATE INDEX IF NOT EXISTS idx_players_weak_foot ON players(weak_foot);
CREATE INDEX IF NOT EXISTS idx_players_club ON players(club);
CREATE INDEX IF NOT EXISTS idx_players_league ON players(league);
CREATE INDEX IF NOT EXISTS idx_players_nationality ON players(nationality);
"""


def get_db_path(custom_path: Optional[str] = None) -> str:
    """Retourne le chemin vers le fichier SQLite."""
    if custom_path:
        return custom_path
    try:
        if current_app and "DATABASE_PATH" in current_app.config:
            return current_app.config["DATABASE_PATH"]
    except RuntimeError:
        # En dehors du contexte d'application Flask
        pass
    return Config.DATABASE_PATH


def get_db(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Retourne la connexion SQLite active.
    Utilise le contexte Flask `g` s'il est disponible, ou ouvre une nouvelle connexion.
    """
    path = get_db_path(db_path)

    # Si nous sommes dans une requête Flask
    try:
        if current_app:
            if "db" not in g:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                g.db = sqlite3.connect(path, timeout=30.0)
                g.db.row_factory = sqlite3.Row
                g.db.execute("PRAGMA journal_mode = WAL;")
                g.db.execute("PRAGMA synchronous = NORMAL;")
                g.db.execute("PRAGMA foreign_keys = ON;")
            return g.db
    except RuntimeError:
        pass

    # Connexion hors contexte Flask (scripts, tests, worker)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def close_db(e=None):
    """Ferme la connexion de la requête Flask en fin de cycle de vie."""
    db = g.pop("db", None) if "db" in g else None
    if db is not None:
        db.close()


def _clean_int(val, default: int = 0) -> int:
    """Nettoie et convertit une valeur en entier sécurisé."""
    if val is None or val == "":
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def import_csv_to_db(
    conn: sqlite3.Connection,
    csv_path: Optional[str] = None,
    force: bool = False
) -> int:
    """
    Importe les données du fichier CSV dans la table SQLite 'players'.
    Retourne le nombre de joueurs importés.
    """
    target_csv = csv_path or Config.CSV_PATH

    cursor = conn.cursor()

    # Vérification si la table contient déjà des données
    cursor.execute("SELECT COUNT(*) FROM players")
    existing_count = cursor.fetchone()[0]

    if existing_count > 0 and not force:
        return existing_count

    if not os.path.exists(target_csv):
        print(f"⚠️ Fichier CSV introuvable à l'emplacement : {target_csv}")
        return existing_count

    if force:
        cursor.execute("DELETE FROM players")
        conn.commit()

    players_data = []

    with open(target_csv, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            try:
                external_id = _clean_int(row.get("player_id"), idx)
                name = row.get("short_name") or row.get("name") or f"Joueur {idx}"
                full_name = row.get("long_name") or name
                overall = _clean_int(row.get("overall") or row.get("overall_rating"), 75)

                raw_pos = row.get("player_positions") or row.get("position") or "BU"
                positions_list = [p.strip().upper() for p in raw_pos.split(",") if p.strip()]
                main_pos = positions_list[0] if positions_list else "BU"
                positions_str = ", ".join(positions_list) if positions_list else main_pos

                club = (row.get("club_name") or "Club Libre").strip()
                league = (row.get("league_name") or "Ligue Internationale").strip()
                nationality = (row.get("nationality_name") or "Monde").strip()

                price = _clean_int(row.get("value_eur"), 150000)

                # Gestion spécifique des Gardiens de but (GK) si les stats classiques sont vides
                is_gk = "GK" in positions_list or "G" in positions_list or main_pos in ("GK", "G")
                pace = _clean_int(row.get("pace"), _clean_int(row.get("goalkeeping_speed"), 60) if is_gk else 70)
                shooting = _clean_int(row.get("shooting"), _clean_int(row.get("goalkeeping_kicking"), 60) if is_gk else 65)
                passing = _clean_int(row.get("passing"), _clean_int(row.get("goalkeeping_handling"), 60) if is_gk else 65)
                dribbling = _clean_int(row.get("dribbling"), _clean_int(row.get("goalkeeping_reflexes"), 60) if is_gk else 65)
                defending = _clean_int(row.get("defending"), _clean_int(row.get("goalkeeping_positioning"), 60) if is_gk else 60)
                physic = _clean_int(row.get("physic"), _clean_int(row.get("goalkeeping_diving"), 60) if is_gk else 70)

                weak_foot = _clean_int(row.get("weak_foot"), 3)
                skill_moves = _clean_int(row.get("skill_moves"), 3)
                img = row.get("player_face_url") or row.get("image_url") or ""

                players_data.append((
                    external_id,
                    name,
                    full_name,
                    overall,
                    main_pos,
                    positions_str,
                    club,
                    league,
                    nationality,
                    price,
                    pace,
                    shooting,
                    passing,
                    dribbling,
                    defending,
                    physic,
                    weak_foot,
                    skill_moves,
                    img
                ))
            except Exception:
                continue

    insert_sql = """
    INSERT INTO players (
        external_id, name, full_name, overall, position, positions,
        club, league, nationality, price,
        pace, shooting, passing, dribbling, defending, physic,
        weak_foot, skill_moves, image_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, players_data)
    conn.commit()

    return len(players_data)


def init_db(
    db_path: Optional[str] = None,
    csv_path: Optional[str] = None,
    force: bool = False
) -> int:
    """
    Initialise le schéma de la base SQLite et importe les données CSV si nécessaire.
    """
    conn = get_db(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    count = import_csv_to_db(conn, csv_path=csv_path, force=force)
    return count


def init_app(app: Flask):
    """
    Enregistre les hooks Flask et la commande CLI `flask init-db`.
    """
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    @click.option("--force", is_flag=True, help="Écrase et recharge complètement la base SQLite.")
    def init_db_command(force: bool):
        """Initialise la base de données SQLite depuis le fichier CSV."""
        with app.app_context():
            db_path = app.config.get("DATABASE_PATH")
            csv_path = app.config.get("CSV_PATH")
            count = init_db(db_path=db_path, csv_path=csv_path, force=force)
            click.echo(f"✅ Base de données SQLite initialisée avec succès ({count} joueurs) dans : {db_path}")


if __name__ == "__main__":
    # Permet d'exécuter `python -m app.database` directement
    count = init_db(force=True)
    print(f"✅ Initialisation directe terminée : {count} joueurs importés dans la base SQLite.")

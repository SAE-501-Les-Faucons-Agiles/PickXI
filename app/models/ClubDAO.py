
import sqlite3
from pathlib import Path

from app.models.Club import Club
from app.models.ClubDAOInterface import ClubDAOInterface


class ClubSqliteDAO(ClubDAOInterface):
    """
    Club data access object dédié à SQLite
    """

    def __init__(self):
        self.databasename = str(
            Path(__file__).resolve().parents[1]
            / "database" / "football_reco.db"
        )

    def _getDbConnection(self):
        """Connexion à la base de données"""
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def findAll(self):
        """Trouve tous les clubs"""

        conn = self._getDbConnection()

        clubs = conn.execute("""
            SELECT
                c.id,
                c.name,
                l.name AS league
            FROM clubs c
            LEFT JOIN leagues l
                ON c.league_id = l.id
            ORDER BY c.name
        """).fetchall()

        conn.close()

        instances = list()

        for club in clubs:
            instances.append(Club(dict(club)))

        return instances

    def findById(self, club_id):
        """Trouve un club par son identifiant"""

        conn = self._getDbConnection()

        club = conn.execute("""
            SELECT
                c.id,
                c.name,
                l.name AS league
            FROM clubs c
            LEFT JOIN leagues l
                ON c.league_id = l.id
            WHERE c.id = :id
        """, {
            "id": club_id
        }).fetchone()

        conn.close()

        if club:
            return Club(dict(club))

        return None

    def findByNameSubword(self, name):
        """Recherche un club par son nom"""

        conn = self._getDbConnection()

        clubs = conn.execute("""
            SELECT
                c.id,
                c.name,
                l.name AS league
            FROM clubs c
            LEFT JOIN leagues l
                ON c.league_id = l.id
            WHERE c.name LIKE :pattern
            ORDER BY c.name
        """, {
            "pattern": f"%{name}%"
        }).fetchall()

        conn.close()

        return [
            Club(dict(club)) for club in clubs
        ]

    def findByLeague(self, league_id):
        """Trouve les clubs d'un championnat"""

        conn = self._getDbConnection()

        clubs = conn.execute("""
            SELECT
                c.id,
                c.name,
                l.name AS league
            FROM clubs c
            LEFT JOIN leagues l
                ON c.league_id = l.id
            WHERE c.league_id = :league_id
            ORDER BY c.name
        """, {
            "league_id": league_id
        }).fetchall()

        conn.close()

        return [
            Club(dict(club)) for club in clubs
        ]

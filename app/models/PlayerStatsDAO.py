
import sqlite3
from pathlib import Path

from app.models.PlayerStats import PlayerStats
from app.models.PlayerStatsDAOInterface import PlayerStatsDAOInterface


class PlayerStatsSqliteDAO(PlayerStatsDAOInterface):
    """
    PlayerStats data access object dédié à SQLite
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

    def findAll(self, edition="FC26"):
        """Trouve toutes les statistiques des joueurs"""

        conn = self._getDbConnection()

        stats = conn.execute("""
            SELECT
                p.sofifa_id,
                p.name,
                ge.code AS edition,
                pe.overall,
                pe.potential,
                ps.*
            FROM player_stats ps
            JOIN player_editions pe
                ON pe.id = ps.player_edition_id
            JOIN players p
                ON p.id = pe.player_id
            JOIN game_editions ge
                ON ge.id = pe.edition_id
            WHERE ge.code = :edition
            ORDER BY pe.overall DESC
        """, {
            "edition": edition
        }).fetchall()

        conn.close()

        instances = list()

        for stat in stats:
            instances.append(PlayerStats(dict(stat)))

        return instances

    def findByPlayerId(self, sofifa_id, edition="FC26"):
        """Trouve les statistiques d'un joueur"""

        conn = self._getDbConnection()

        stats = conn.execute("""
            SELECT
                p.sofifa_id,
                p.name,
                ge.code AS edition,
                pe.overall,
                pe.potential,
                ps.*
            FROM player_stats ps
            JOIN player_editions pe
                ON pe.id = ps.player_edition_id
            JOIN players p
                ON p.id = pe.player_id
            JOIN game_editions ge
                ON ge.id = pe.edition_id
            WHERE p.sofifa_id = :sofifa_id
            AND ge.code = :edition
        """, {
            "sofifa_id": sofifa_id,
            "edition": edition
        }).fetchone()

        conn.close()

        if stats:
            return PlayerStats(dict(stats))

        return None


import sqlite3
from pathlib import Path

from app.models.Player import Player
from app.models.PlayerDAOInterface import PlayerDAOInterface


class PlayerSqliteDAO(PlayerDAOInterface):
    """
    Player data access object dédié à SQLite
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
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def findAll(self, edition="FC26"):
        """Trouve tous les joueurs d'une édition"""

        conn = self._getDbConnection()

        players = conn.execute("""
            SELECT *
            FROM v_recommendations
            WHERE edition = :edition
            ORDER BY overall DESC
        """, {"edition": edition}).fetchall()

        conn.close()

        instances = list()

        for player in players:
            instances.append(Player(dict(player)))

        return instances

    def findById(self, sofifa_id, edition="FC26"):
        """Trouve un joueur par son ID SoFIFA"""

        conn = self._getDbConnection()

        player = conn.execute("""
            SELECT *
            FROM v_recommendations
            WHERE sofifa_id = :id
            AND edition = :edition
        """, {
            "id": sofifa_id,
            "edition": edition
        }).fetchone()

        conn.close()

        if player:
            return Player(dict(player))

        return None

    def findByNameSubword(self, name, edition="FC26"):
        """Recherche les joueurs contenant le nom indiqué"""

        conn = self._getDbConnection()

        players = conn.execute("""
            SELECT *
            FROM v_recommendations
            WHERE name LIKE :pattern
            AND edition = :edition
            ORDER BY overall DESC
        """, {
            "pattern": f"%{name}%",
            "edition": edition
        }).fetchall()

        conn.close()

        instances = [
            Player(dict(player)) for player in players
        ]

        return instances

    def findByCriteria(self, edition="FC26",
                       position=None, min_overall=None,
                       max_age=None, max_budget=None,
                       min_pace=None):
        """
        Recherche les joueurs selon les critères
        sélectionnés par l'utilisateur.
        """

        conn = self._getDbConnection()

        query = """
            SELECT *
            FROM v_recommendations v
            WHERE v.edition = :edition
        """

        params = {"edition": edition}

        if position:
            query += """
                AND EXISTS (
                    SELECT 1
                    FROM players p
                    JOIN player_editions pe
                        ON pe.player_id = p.id
                    JOIN game_editions ge
                        ON ge.id = pe.edition_id
                    JOIN player_positions pp
                        ON pp.player_edition_id = pe.id
                    WHERE p.sofifa_id = v.sofifa_id
                    AND ge.code = v.edition
                    AND pp.position_code = :position
                )
            """
            params["position"] = position.upper()

        if min_overall is not None:
            query += " AND v.overall >= :min_overall"
            params["min_overall"] = min_overall

        if max_age is not None:
            query += " AND v.age <= :max_age"
            params["max_age"] = max_age

        if max_budget is not None:
            query += """
                AND v.market_value_eur <= :max_budget
            """
            params["max_budget"] = max_budget

        if min_pace is not None:
            query += " AND v.pace >= :min_pace"
            params["min_pace"] = min_pace

        query += " ORDER BY v.overall DESC"

        players = conn.execute(
            query, params
        ).fetchall()

        conn.close()

        instances = [
            Player(dict(player)) for player in players
        ]

        return instances

    def getNumberOfElements(self, edition="FC26"):
        """Retourne le nombre de joueurs"""

        conn = self._getDbConnection()

        result = conn.execute("""
            SELECT COUNT(*) AS total
            FROM v_recommendations
            WHERE edition = :edition
        """, {"edition": edition}).fetchone()

        conn.close()

        return result["total"]

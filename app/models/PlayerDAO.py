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

        return [Player(dict(player)) for player in players]

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

        return [Player(dict(player)) for player in players]

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
            query += " AND v.market_value_eur <= :max_budget"
            params["max_budget"] = max_budget

        if min_pace is not None:
            query += " AND v.pace >= :min_pace"
            params["min_pace"] = min_pace

        query += " ORDER BY v.overall DESC"

        players = conn.execute(query, params).fetchall()
        conn.close()

        return [Player(dict(player)) for player in players]

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

    def findCandidatesForScoring(
        self,
        edition="FC26",
        q=None,
        position=None,
        max_budget=None,
        max_age=None,
        preferred_foot=None,
        league=None,
        min_overall = None
    ):
        """
        Récupère les joueurs correspondant aux filtres stricts (barrages)
        avec toutes les colonnes nécessaires à l'algorithme de scoring.
        """
        conn = self._getDbConnection()

        query = """
            SELECT
                v.*,
                pe.weak_foot,
                pe.skill_moves,
                pe.preferred_foot,
                lg.name AS league,
                COALESCE(
                    (
                        SELECT GROUP_CONCAT(ps.name, ',')
                        FROM player_playstyles pps
                        JOIN playstyles ps ON ps.id = pps.playstyle_id
                        WHERE pps.player_edition_id = pe.id
                    ),
                    ''
                ) AS player_traits
            FROM v_recommendations v
            JOIN players p ON p.sofifa_id = v.sofifa_id
            JOIN game_editions ge ON ge.code = v.edition
            JOIN player_editions pe ON pe.player_id = p.id AND pe.edition_id = ge.id
            LEFT JOIN clubs c ON c.id = pe.club_id
            LEFT JOIN leagues lg ON lg.id = c.league_id
            WHERE v.edition = :edition
        """
        params = {"edition": edition}

        # Filtre texte (nom, club ou pays)
        if q:
            query += """
                AND (
                    LOWER(v.name) LIKE :q
                    OR LOWER(COALESCE(v.club, '')) LIKE :q
                    OR LOWER(COALESCE(v.nationality, '')) LIKE :q
                )
            """
            params["q"] = f"%{q.lower()}%"

        # Filtre strict : Poste
        if position and position != "ALL":
            query += """
                AND EXISTS (
                    SELECT 1
                    FROM player_positions pp
                    WHERE pp.player_edition_id = pe.id
                    AND pp.position_code = :position
                )
            """
            params["position"] = position.upper()

        # Filtre strict : Budget max (garde aussi les joueurs sans prix renseigné)
        if max_budget is not None:
            query += " AND (v.market_value_eur IS NULL OR v.market_value_eur <= :max_budget)"
            params["max_budget"] = max_budget

        # Filtre strict : Âge max
        if max_age is not None:
            query += " AND (v.age IS NULL OR v.age <= :max_age)"
            params["max_age"] = max_age

        #Filtre strict : général
        if min_overall is not None:
            query += " AND v.overall >= :min_overall"
            params["min_overall"] = min_overall
        # Filtre strict : Pied fort
        if preferred_foot:
            query += " AND LOWER(COALESCE(pe.preferred_foot, '')) = :preferred_foot"
            params["preferred_foot"] = preferred_foot.lower()

        # Filtre strict : Championnat
        if league and league != "ALL":
            query += " AND LOWER(COALESCE(lg.name, '')) = :league"
            params["league"] = league.lower()

        rows = conn.execute(query, params).fetchall()
        conn.close()

        return [dict(row) for row in rows]
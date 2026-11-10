
import sqlite3
from pathlib import Path

from app.models.ReferenceDAOInterface import ReferenceDAOInterface


class ReferenceSqliteDAO(ReferenceDAOInterface):
    """
    DAO des données de référence dédié à SQLite
    Le ReferenceDAO sert à récupérer les différentes options 
    que l'utilisateur pourra sélectionner dans l'app pour effectuer une recommandation  .
    ex : ['ST', 'CM', 'CB', 'LW', ...] ou encore ['Ligue 1', 'Premier League', 'La Liga', ...]
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

    def getUniquePositions(self):
        """Trouve tous les postes"""

        conn = self._getDbConnection()

        positions = conn.execute("""
            SELECT code
            FROM positions
            ORDER BY code
        """).fetchall()

        conn.close()

        return [p["code"] for p in positions]

    def getUniqueCountries(self):
        """Trouve toutes les nationalités"""

        conn = self._getDbConnection()

        countries = conn.execute("""
            SELECT name
            FROM countries
            ORDER BY name
        """).fetchall()

        conn.close()

        return [c["name"] for c in countries]

    def getUniqueLeagues(self):
        """Trouve tous les championnats"""

        conn = self._getDbConnection()

        leagues = conn.execute("""
            SELECT name
            FROM leagues
            ORDER BY name
        """).fetchall()

        conn.close()

        return [l["name"] for l in leagues]

    def getUniquePlaystyles(self):
        """Trouve tous les PlayStyles"""

        conn = self._getDbConnection()

        styles = conn.execute("""
            SELECT name
            FROM playstyles
            ORDER BY name
        """).fetchall()

        conn.close()

        return [s["name"] for s in styles]

    def getUniqueEditions(self):
        """Trouve toutes les éditions EA FC"""

        conn = self._getDbConnection()

        editions = conn.execute("""
            SELECT code
            FROM game_editions
            ORDER BY code DESC
        """).fetchall()

        conn.close()

        return [e["code"] for e in editions]

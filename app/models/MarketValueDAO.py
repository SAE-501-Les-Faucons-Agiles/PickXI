
import sqlite3
from pathlib import Path

from app.models.MarketValue import MarketValue
from app.models.MarketValueDAOInterface import MarketValueDAOInterface


class MarketValueSqliteDAO(MarketValueDAOInterface):
    """
    MarketValue data access object dédié à SQLite
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

    def findByPlayerId(self, sofifa_id):
        """Trouve la dernière valeur marchande d'un joueur"""

        conn = self._getDbConnection()

        value = conn.execute("""
            SELECT
                tm.tm_player_id,
                tm.name,
                COALESCE(
                    mv.value_eur,
                    tm.current_market_value_eur
                ) AS value_eur,
                mv.valuation_date,
                link.method
            FROM players p
            JOIN player_links link
                ON link.player_id = p.id
            JOIN tm_players tm
                ON tm.tm_player_id = link.tm_player_id
            LEFT JOIN market_values mv
                ON mv.tm_player_id = tm.tm_player_id
                AND mv.valuation_date = (
                    SELECT MAX(m2.valuation_date)
                    FROM market_values m2
                    WHERE m2.tm_player_id = tm.tm_player_id
                )
            WHERE p.sofifa_id = :sofifa_id
        """, {
            "sofifa_id": sofifa_id
        }).fetchone()

        conn.close()

        if value:
            return MarketValue(dict(value))

        return None

    def findHistoryByPlayerId(self, sofifa_id):
        """Trouve l'historique des valeurs marchandes"""

        conn = self._getDbConnection()

        values = conn.execute("""
            SELECT
                tm.tm_player_id,
                tm.name,
                mv.value_eur,
                mv.valuation_date,
                link.method
            FROM market_values mv
            JOIN tm_players tm
                ON tm.tm_player_id = mv.tm_player_id
            JOIN player_links link
                ON link.tm_player_id = tm.tm_player_id
            JOIN players p
                ON p.id = link.player_id
            WHERE p.sofifa_id = :sofifa_id
            ORDER BY mv.valuation_date DESC
        """, {
            "sofifa_id": sofifa_id
        }).fetchall()

        conn.close()

        instances = list()

        for value in values:
            instances.append(MarketValue(dict(value)))

        return instances

    def addValue(self, tm_player_id, date, value_eur):
        """Ajoute ou actualise une valeur marchande"""

        if value_eur < 0:
            return False

        conn = self._getDbConnection()

        try:
            conn.execute("""
                INSERT INTO market_values(
                    tm_player_id,
                    valuation_date,
                    value_eur
                )
                VALUES (
                    :tm_player_id,
                    :date,
                    :value_eur
                )
                ON CONFLICT(tm_player_id, valuation_date)
                DO UPDATE SET
                    value_eur = excluded.value_eur
            """, {
                "tm_player_id": tm_player_id,
                "date": date,
                "value_eur": value_eur
            })

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            conn.rollback()
            return False

        finally:
            conn.close()

import unittest
import os
import sqlite3
from app.config import Config
from app.database import get_db, init_db, SCHEMA_SQL
from app.models.player_model import Player, PlayerFilter


class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Utilisation de la base SQLite existante ou initialisée
        cls.db_path = Config.DATABASE_PATH
        cls.conn = get_db(cls.db_path)

    def test_database_table_exists(self):
        """Vérifie que la table players existe dans SQLite."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
        table = cursor.fetchone()
        self.assertIsNotNone(table)
        self.assertEqual(table[0], "players")

    def test_database_indexes_exist(self):
        """Vérifie que les index d'optimisation sont bien créés."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        self.assertIn("idx_players_overall", indexes)
        self.assertIn("idx_players_position", indexes)
        self.assertIn("idx_players_price", indexes)

    def test_player_count_sql(self):
        """Vérifie la requête SQL COUNT(*)."""
        count = Player.count(conn=self.conn)
        self.assertGreater(count, 15000)

    def test_player_find_by_id_sql(self):
        """Vérifie la requête SQL SELECT * FROM players WHERE id = ?."""
        player = Player.find_by_id(1, conn=self.conn)
        self.assertIsNotNone(player)
        self.assertIsInstance(player, Player)
        self.assertGreater(player.overall, 0)
        self.assertTrue(len(player.name) > 0)

    def test_player_find_all_pagination_sql(self):
        """Vérifie la pagination SQL LIMIT ? OFFSET ?."""
        page1 = Player.find_all(limit=10, offset=0, conn=self.conn)
        page2 = Player.find_all(limit=10, offset=10, conn=self.conn)
        self.assertEqual(len(page1), 10)
        self.assertEqual(len(page2), 10)
        self.assertNotEqual(page1[0].id, page2[0].id)

    def test_player_search_like_sql(self):
        """Vérifie la recherche textuelle avec SQL LIKE."""
        results = Player.find_all(search="Mbapp", conn=self.conn)
        self.assertGreater(len(results), 0)
        has_mbappe = any("Mbapp" in p.name or "Mbapp" in p.full_name for p in results)
        self.assertTrue(has_mbappe)

    def test_player_find_candidates_sql(self):
        """Vérifie le filtrage multi-critères SQL (prix, mauvais pied, poste)."""
        flt = PlayerFilter(
            position="BU",
            max_price=5000000,
            min_weak_foot=3
        )
        candidates = Player.find_candidates(flt, limit=10, conn=self.conn)
        self.assertGreater(len(candidates), 0)
        for c in candidates:
            self.assertLessEqual(c.price, 5000000)
            self.assertGreaterEqual(c.weak_foot, 3)

    def test_player_distinct_metadata_sql(self):
        """Vérifie les requêtes SQL SELECT DISTINCT sur les clubs, ligues et nations."""
        clubs = Player.get_unique_clubs(conn=self.conn)
        leagues = Player.get_unique_leagues(conn=self.conn)
        nations = Player.get_unique_nationalities(conn=self.conn)

        self.assertGreater(len(clubs), 50)
        self.assertGreater(len(leagues), 10)
        self.assertGreater(len(nations), 30)
        self.assertIn("Real Madrid", clubs)


if __name__ == "__main__":
    unittest.main()

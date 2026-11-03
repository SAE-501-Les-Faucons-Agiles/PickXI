import unittest
from app import create_app
from app.models.player_model import PlayerFilter
from app.services.recommendation_service import recommendation_service

class RecommendationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("default")
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"FUTScout", response.data)
        self.assertIn(b"Tableau de Bord", response.data)

    def test_players_page(self):
        response = self.client.get("/players")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mbapp", response.data)

    def test_about_page(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Kaggle", response.data)

    def test_api_players(self):
        response = self.client.get("/api/v1/players")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["count"], 0)

    def test_api_recommend(self):
        payload = {
            "position": "BU",
            "max_price": 3000000,
            "min_weak_foot": 3,
            "target_club": "Real Madrid"
        }
        response = self.client.post("/api/v1/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("vector_cosine", data["approaches"])
        self.assertIn("chemistry_graph", data["approaches"])
        self.assertGreater(len(data["approaches"]["vector_cosine"]["ranked_players"]), 0)

    def test_service_comparison(self):
        flt = PlayerFilter(position="BU", max_price=3000000, min_weak_foot=3)
        res = recommendation_service.run_comparison(flt, limit=4)
        self.assertIn("vector_cosine", res)
        self.assertIn("chemistry_graph", res)
        self.assertGreater(len(res["vector_cosine"].ranked_players), 0)

if __name__ == "__main__":
    unittest.main()

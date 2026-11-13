from app.services.PlayerService import PlayerService


class PitchService:
    """
    Service gérant la tactique de terrain (Mon Onze) :
    Formations, suggestions de pépites par poste et métriques d'équipe.
    """

    FORMATIONS = {
        "4-3-3": [
            {"pos": "GK", "top": "88%", "left": "50%"},
            {"pos": "LB", "top": "72%", "left": "15%"},
            {"pos": "CB", "top": "75%", "left": "38%"},
            {"pos": "CB", "top": "75%", "left": "62%"},
            {"pos": "RB", "top": "72%", "left": "85%"},
            {"pos": "CDM", "top": "54%", "left": "50%"},
            {"pos": "CM", "top": "42%", "left": "30%"},
            {"pos": "CM", "top": "42%", "left": "70%"},
            {"pos": "LW", "top": "20%", "left": "18%"},
            {"pos": "ST", "top": "14%", "left": "50%"},
            {"pos": "RW", "top": "20%", "left": "82%"}
        ],
        "4-2-3-1": [
            {"pos": "GK", "top": "88%", "left": "50%"},
            {"pos": "LB", "top": "72%", "left": "15%"},
            {"pos": "CB", "top": "75%", "left": "38%"},
            {"pos": "CB", "top": "75%", "left": "62%"},
            {"pos": "RB", "top": "72%", "left": "85%"},
            {"pos": "CDM", "top": "58%", "left": "35%"},
            {"pos": "CDM", "top": "58%", "left": "65%"},
            {"pos": "CAM", "top": "35%", "left": "50%"},
            {"pos": "LM", "top": "32%", "left": "18%"},
            {"pos": "RM", "top": "32%", "left": "82%"},
            {"pos": "ST", "top": "14%", "left": "50%"}
        ],
        "4-4-2": [
            {"pos": "GK", "top": "88%", "left": "50%"},
            {"pos": "LB", "top": "72%", "left": "15%"},
            {"pos": "CB", "top": "75%", "left": "38%"},
            {"pos": "CB", "top": "75%", "left": "62%"},
            {"pos": "RB", "top": "72%", "left": "85%"},
            {"pos": "LM", "top": "46%", "left": "16%"},
            {"pos": "CM", "top": "50%", "left": "38%"},
            {"pos": "CM", "top": "50%", "left": "62%"},
            {"pos": "RM", "top": "46%", "left": "84%"},
            {"pos": "ST", "top": "18%", "left": "38%"},
            {"pos": "ST", "top": "18%", "left": "62%"}
        ],
        "3-5-2": [
            {"pos": "GK", "top": "88%", "left": "50%"},
            {"pos": "CB", "top": "74%", "left": "26%"},
            {"pos": "CB", "top": "76%", "left": "50%"},
            {"pos": "CB", "top": "74%", "left": "74%"},
            {"pos": "CDM", "top": "56%", "left": "38%"},
            {"pos": "CDM", "top": "56%", "left": "62%"},
            {"pos": "LM", "top": "42%", "left": "14%"},
            {"pos": "CAM", "top": "34%", "left": "50%"},
            {"pos": "RM", "top": "42%", "left": "86%"},
            {"pos": "ST", "top": "16%", "left": "38%"},
            {"pos": "ST", "top": "16%", "left": "62%"}
        ]
    }

    def __init__(self, player_service=None):
        self.player_service = player_service or PlayerService()

    def get_formation(self, formation_name="4-3-3"):
        """Retourne la disposition des postes et coordonnées d'un dispositif"""
        return self.FORMATIONS.get(formation_name, self.FORMATIONS["4-3-3"])

    def get_recommendations_for_slot(self, position_code="ST", limit=4):
        """Propose les meilleures options pour un poste précis du terrain"""
        filters = {
            "pos": position_code,
            "min_ovr": 82,
            "sort": "overall_desc"
        }
        res = self.player_service.search_players(filters, page=1, per_page=limit)
        return res["players"]

    def calculate_squad_metrics(self, player_ids):
        """Calcule la note générale moyenne, la vitesse et le coût cumulé du onze"""
        if not player_ids:
            return {"overall": 0, "pace": 0, "cost": 0, "formatted_cost": "0 €"}

        total_ovr = 0
        total_pace = 0
        total_cost = 0
        valid_count = 0

        for pid in player_ids:
            p, _ = self.player_service.get_player_by_id(pid)
            if p:
                total_ovr += p.get("overall", 0)
                total_pace += p.get("pace", 0)
                total_cost += p.get("market_value_eur", 0)
                valid_count += 1

        if valid_count == 0:
            return {"overall": 0, "pace": 0, "cost": 0, "formatted_cost": "0 €"}

        avg_ovr = round(total_ovr / valid_count)
        avg_pace = round(total_pace / valid_count)
        cost_m = round(total_cost / 1000000, 1)

        return {
            "overall": avg_ovr,
            "pace": avg_pace,
            "cost": total_cost,
            "formatted_cost": f"{cost_m}M €" if cost_m >= 1 else f"{round(total_cost/1000)}k €"
        }

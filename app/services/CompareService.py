from app.services.PlayerService import PlayerService


class CompareService:
    """
    Service dédié à la comparaison 1 contre 1 entre deux joueurs :
    Calcul des écarts, génération des jeux de données radar SVG et analyse synthétique.
    """

    def __init__(self, player_service=None):
        self.player_service = player_service or PlayerService()

    def compare_players(self, player1_id=252371, player2_id=239053):
        """Compare deux joueurs par leurs identifiants SoFIFA"""
        p1, _ = self.player_service.get_player_by_id(player1_id)
        p2, _ = self.player_service.get_player_by_id(player2_id)

        # Fallback par défaut si non trouvés
        if not p1:
            p1 = self.player_service.get_curated_players(1)[0]
        if not p2:
            curated = self.player_service.get_curated_players(2)
            p2 = curated[1] if len(curated) > 1 else curated[0]

        # Données du radar 6 axes [PAC, SHO, PAS, DRI, DEF, PHY]
        radar1 = [
            p1.get("pace", 75), p1.get("shooting", 75), p1.get("passing", 75),
            p1.get("dribbling", 75), p1.get("defending", 75), p1.get("physicality", 75)
        ]
        radar2 = [
            p2.get("pace", 75), p2.get("shooting", 75), p2.get("passing", 75),
            p2.get("dribbling", 75), p2.get("defending", 75), p2.get("physicality", 75)
        ]

        # Écarts par attribut
        diffs = {
            "pace": p1.get("pace", 75) - p2.get("pace", 75),
            "shooting": p1.get("shooting", 75) - p2.get("shooting", 75),
            "passing": p1.get("passing", 75) - p2.get("passing", 75),
            "dribbling": p1.get("dribbling", 75) - p2.get("dribbling", 75),
            "defending": p1.get("defending", 75) - p2.get("defending", 75),
            "physicality": p1.get("physicality", 75) - p2.get("physicality", 75),
        }

        # Synthèse analytique du duel
        summary = self._generate_summary(p1, p2, diffs)

        return {
            "p1": p1,
            "p2": p2,
            "radar1": radar1,
            "radar2": radar2,
            "diffs": diffs,
            "summary": summary
        }

    def _generate_summary(self, p1, p2, diffs):
        """Rédige une analyse objective de comparaison"""
        p1_name = p1.get("name", "Joueur 1")
        p2_name = p2.get("name", "Joueur 2")

        if diffs["pace"] >= 4:
            return f"<strong>{p1_name}</strong> a un avantage net en vitesse de pointe et en transition rapide (+{diffs['pace']} PAC) par rapport à {p2_name}."
        elif diffs["pace"] <= -4:
            return f"<strong>{p2_name}</strong> domine largement sur le plan de la vitesse pure et de l'accélération (+{-diffs['pace']} PAC)."
        elif diffs["defending"] >= 5:
            return f"<strong>{p1_name}</strong> offre une assise défensive bien supérieure (+{diffs['defending']} DEF) et récupère plus de ballons dans les duels."
        elif diffs["defending"] <= -5:
            return f"<strong>{p2_name}</strong> est bien plus fiable en phase de repli défensif et tacles (+{-diffs['defending']} DEF)."
        elif diffs["shooting"] >= 4:
            return f"<strong>{p1_name}</strong> se montre nettement plus tranchant et décisif devant le but (+{diffs['shooting']} SHO)."
        elif diffs["shooting"] <= -4:
            return f"<strong>{p2_name}</strong> possède une meilleure puissance de frappe et précision à la finition (+{-diffs['shooting']} SHO)."
        else:
            return f"Les deux joueurs affichent un niveau très proche ({p1.get('overall', 85)} vs {p2.get('overall', 85)}). Le choix dépendra surtout de leur position préférentielle et des liens de collectif."

    def search_candidates(self, query=None, position=None, exclude_id=None, limit=20):
        """Recherche rapide de joueurs pour le sélecteur du comparateur"""
        filters = {
            "q": query or "",
            "pos": position or "ALL",
            "sort": "overall_desc"
        }
        res = self.player_service.search_players(filters, page=1, per_page=limit + 5)
        candidates = [p for p in res["players"] if p["sofifa_id"] != exclude_id]
        return candidates[:limit]

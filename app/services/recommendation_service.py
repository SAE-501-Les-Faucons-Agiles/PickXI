import math
from typing import List, Dict, Any, Optional
from app.models.player_model import (
    Player,
    PlayerFilter,
    RankedPlayer,
    PerformanceMetrics,
    RecommendationResult
)
from app.services.player_repository import player_repository
from app.services.metrics_service import metrics_service

class VectorCosineRecommender:
    """
    Approche 1 : Modèle d'Espace Vectoriel & Distance Cosinus
    Projette chaque joueur dans un espace à 7 dimensions (PAC, SHO, PAS, DRI, DEF, PHY, WF).
    Calcule la similarité cosinus avec le vecteur de statistiques souhaité par le joueur.
    Complexité : O(N * D)
    """

    @staticmethod
    def recommend(
        players: List[Player],
        player_filter: PlayerFilter,
        limit: int = 6
    ) -> List[RankedPlayer]:
        # Vecteur de requête de l'utilisateur
        user_vector = [
            player_filter.weight_pace,
            player_filter.weight_shooting,
            player_filter.weight_passing,
            player_filter.weight_dribbling,
            player_filter.weight_defending,
            player_filter.weight_physic,
            player_filter.min_weak_foot / 5.0
        ]
        norm_user = math.sqrt(sum(x * x for x in user_vector)) or 1.0

        candidates = []
        for p in players:
            # Filtre de budget
            if p.price > player_filter.max_price:
                continue
            # Filtre de mauvais pied
            if p.weak_foot < player_filter.min_weak_foot:
                continue
            # Filtre de poste
            if player_filter.position != "ALL" and player_filter.position not in p.positions and player_filter.position != p.position:
                continue

            # Vecteur normalisé du joueur
            p_vector = [
                p.pace / 99.0,
                p.shooting / 99.0,
                p.passing / 99.0,
                p.dribbling / 99.0,
                p.defending / 99.0,
                p.physic / 99.0,
                p.weak_foot / 5.0
            ]
            norm_p = math.sqrt(sum(x * x for x in p_vector)) or 1.0

            # Produit scalaire
            dot_product = sum(u * v for u, v in zip(user_vector, p_vector))
            cosine_sim = dot_product / (norm_user * norm_p)

            # Collectif indicatif (sans peser sur la décision géométrique)
            chem = 0
            if player_filter.target_club and p.club == player_filter.target_club:
                chem += 3
            if player_filter.target_league and p.league == player_filter.target_league:
                chem += 2
            if player_filter.target_nationality and p.nationality == player_filter.target_nationality:
                chem += 1

            candidates.append(RankedPlayer(
                player=p,
                score=cosine_sim,
                chemistry_points=chem,
                match_percentage=min(100, int(cosine_sim * 100))
            ))

        # Tri décroissant par similarité cosinus
        candidates.sort(key=lambda x: x.score, reverse=True)
        return candidates[:limit]


class ChemistryGraphRecommender:
    """
    Approche 2 : Graphe de Collectif & Heuristique Rentabilité FUT
    Évalue le réseau de synergies (Club +3, Ligue +2, Nation +1)
    et combine avec la note générale et le coût en crédits (Quality / Price Heuristic).
    Complexité : O(N * C + N log K)
    """

    @staticmethod
    def recommend(
        players: List[Player],
        player_filter: PlayerFilter,
        limit: int = 6
    ) -> List[RankedPlayer]:
        candidates = []
        max_price_ref = max(player_filter.max_price, 50000)

        for p in players:
            if p.price > player_filter.max_price:
                continue
            if p.weak_foot < player_filter.min_weak_foot:
                continue
            if player_filter.position != "ALL" and player_filter.position not in p.positions and player_filter.position != p.position:
                continue

            # Calcul des liens de graphe (Chemistry / Synergie)
            chem = 0
            if player_filter.target_club and p.club == player_filter.target_club:
                chem += 3
            if player_filter.target_league and p.league == player_filter.target_league:
                chem += 2
            if player_filter.target_nationality and p.nationality == player_filter.target_nationality:
                chem += 1

            norm_chem = min(1.0, chem / 6.0)
            norm_ovr = p.overall / 99.0

            # Heuristique valeur économique : valorise les joueurs très forts à prix accessible
            price_log = math.log10(max(p.price, 1000))
            max_log = math.log10(max_price_ref * 1.5)
            value_ratio = max(0.0, 1.0 - (price_log / max_log))

            # Score composite FUT
            score = (0.40 * norm_chem) + (0.35 * norm_ovr) + (0.25 * value_ratio)

            match_pct = int(((norm_chem * 0.5) + (norm_ovr * 0.5)) * 100)

            candidates.append(RankedPlayer(
                player=p,
                score=score,
                chemistry_points=chem,
                match_percentage=min(100, max(10, match_pct))
            ))

        # Tri décroissant par score heuristique
        candidates.sort(key=lambda x: x.score, reverse=True)
        return candidates[:limit]


class RecommendationService:
    """
    Orchestrateur de recommandation comparative pour FUTScout.
    Exécute les deux approches et consigne les métriques pour les enseignants évaluateurs.
    """

    def __init__(self):
        self.repository = player_repository

    def get_all_players(self) -> List[Player]:
        return self.repository.get_all()

    def run_comparison(self, player_filter: PlayerFilter, limit: int = 6) -> Dict[str, Any]:
        all_players = self.repository.get_all()

        # 1. Approche Vectorielle (Cosinus)
        res_vec, last_vec, min_vec, max_vec, avg_vec, mem_vec = metrics_service.measure_execution(
            VectorCosineRecommender.recommend,
            "vector_cosine",
            all_players,
            player_filter,
            limit=limit,
            iterations=10
        )
        battery_vec = metrics_service.estimate_battery_impact(avg_vec, mem_vec)

        metrics_vec = PerformanceMetrics(
            execution_time_ms=last_vec,
            time_min_ms=min_vec,
            time_max_ms=max_vec,
            time_avg_ms=avg_vec,
            theoretical_complexity="O(N * D)",
            space_complexity="O(N)",
            memory_usage_kb=mem_vec,
            battery_impact_score=battery_vec,
            comparison_notes="Excellente adéquation morphologique/statistique. Calcul vectoriel direct en O(N * 7)."
        )

        result_vec = RecommendationResult(
            approach_id="vector_cosine",
            approach_name="Similarité Vectorielle (Profil & Cosinus)",
            approach_description="Évalue l'angle vectoriel sur 7 dimensions de caractéristiques athlétiques et techniques.",
            ranked_players=res_vec,
            metrics=metrics_vec
        )

        # 2. Approche Graphe & Heuristique Collectif
        res_chem, last_chem, min_chem, max_chem, avg_chem, mem_chem = metrics_service.measure_execution(
            ChemistryGraphRecommender.recommend,
            "chemistry_graph",
            all_players,
            player_filter,
            limit=limit,
            iterations=10
        )
        battery_chem = metrics_service.estimate_battery_impact(avg_chem, mem_chem)

        metrics_chem = PerformanceMetrics(
            execution_time_ms=last_chem,
            time_min_ms=min_chem,
            time_max_ms=max_chem,
            time_avg_ms=avg_chem,
            theoretical_complexity="O(N * C + N log K)",
            space_complexity="O(N)",
            memory_usage_kb=mem_chem,
            battery_impact_score=battery_chem,
            comparison_notes="Privilégie les liens de collectif (Club/Nation/Ligue) et l'efficience prix/note."
        )

        result_chem = RecommendationResult(
            approach_id="chemistry_graph",
            approach_name="Graphe de Collectif & Rentabilité (Heuristique FUT)",
            approach_description="Explore le réseau de synergie d'équipe et applique une heuristique qualité/prix.",
            ranked_players=res_chem,
            metrics=metrics_chem
        )

        return {
            "filter": player_filter,
            "vector_cosine": result_vec,
            "chemistry_graph": result_chem,
            "total_candidates": len(all_players)
        }

recommendation_service = RecommendationService()

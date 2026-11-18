class ScoringService:
    """
    Service dédié au calcul du score de correspondance (match_score)
    d'un joueur par rapport aux critères cibles de l'utilisateur.
    """

    @staticmethod
    def calculer_score(joueur, cibles_stats, traits_souhaites=None):
        """
        Calcule le score d'un joueur selon ses stats et ses PlayStyles/traits :
        - Sous la cible : forte pénalité (x3, et x5 sur la note générale)
        - Au-dessus de la cible : léger bonus (x0.5)
        - weak_foot & skill_moves : mis à l'échelle x20
        - PlayStyles/Traits : +10 points par trait possédé
        """
        score_total = 0.0

        # 1. Évaluation des statistiques
        for stat, cible in cibles_stats.items():
            if cible is None or cible == "":
                continue

            valeur_joueur = joueur.get(stat)
            valeur_joueur = float(valeur_joueur) if valeur_joueur is not None else 0.0
            cible_val = float(cible)

            diff = valeur_joueur - cible_val

            # Mise à l'échelle pour les notes sur 5
            if stat in ("weak_foot", "skill_moves"):
                diff *= 20.0

            # Poids plus important sur la note générale
            poids = 2.0 if stat == "overall" else 1.0

            if diff < 0:
                # Forte pénalité si le joueur n'atteint pas le critère
                score_total += diff * 3.0 * poids
            else:
                # Léger bonus s'il dépasse le critère
                score_total += diff * 0.5 * poids

        # 2. Évaluation des Traits / PlayStyles (Bonus de +10 par trait possédé)
        if traits_souhaites:
            traits_du_joueur = str(joueur.get("player_traits", "") or "").lower()
            for trait in traits_souhaites:
                if trait and trait.lower() in traits_du_joueur:
                    score_total += 10.0

        return round(score_total, 1)
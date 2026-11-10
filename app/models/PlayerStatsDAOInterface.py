
class PlayerStatsDAOInterface:
    """Interface pour le DAO PlayerStats"""

    def findAll(self, edition="FC26"):
        """Trouve toutes les statistiques des joueurs"""
        pass

    def findByPlayerId(self, sofifa_id, edition="FC26"):
        """Trouve les statistiques d'un joueur"""
        pass

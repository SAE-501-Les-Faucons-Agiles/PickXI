
class MarketValueDAOInterface:
    """Interface pour le DAO MarketValue"""

    def findByPlayerId(self, sofifa_id):
        """Trouve la dernière valeur d'un joueur"""
        pass

    def findHistoryByPlayerId(self, sofifa_id):
        """Trouve l'historique des valeurs d'un joueur"""
        pass

    def addValue(self, tm_player_id, date, value_eur):
        """Ajoute une valeur marchande"""
        pass

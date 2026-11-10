
class PlayerDAOInterface:
    """Interface pour le DAO Player"""

    def findAll(self, edition="FC26"):
        """Trouve tous les joueurs"""
        pass

    def findById(self, sofifa_id, edition="FC26"):
        """Trouve un joueur par son identifiant"""
        pass

    def findByNameSubword(self, name, edition="FC26"):
        """Recherche un joueur par son nom"""
        pass

    def findByCriteria(self, edition="FC26",
                       position=None, min_overall=None,
                       max_age=None, max_budget=None,
                       min_pace=None):
        """Recherche les joueurs selon des critères"""
        pass

    def getNumberOfElements(self, edition="FC26"):
        """Retourne le nombre de joueurs"""
        pass

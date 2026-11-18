
class PlayerDAOInterface:
    """Interface pour le DAO Player"""

    def findAll(self, edition="FC26", limit=None, offset=None):
        """Trouve tous les joueurs"""
        pass

    def findById(self, sofifa_id, edition="FC26"):
        """Trouve un joueur par son identifiant"""
        pass

    def findByNameSubword(self, name, edition="FC26", limit=None, offset=None):
        """Recherche un joueur par son nom"""
        pass

    def findByCriteria(self, edition="FC26",
                       position=None, min_overall=None,
                       max_age=None, max_budget=None,
                       min_pace=None, min_potential=None,
                       min_shooting=None, min_passing=None,
                       min_dribbling=None, min_defending=None,
                       min_physicality=None, name=None,
                       sort="overall_desc", limit=None, offset=None):
        """Recherche les joueurs selon des critères"""
        pass

    def countByCriteria(self, edition="FC26",
                        position=None, min_overall=None,
                        max_age=None, max_budget=None,
                        min_pace=None, min_potential=None,
                        min_shooting=None, min_passing=None,
                        min_dribbling=None, min_defending=None,
                        min_physicality=None, name=None):
        """Compte les joueurs correspondant aux critères"""
        pass

    def getNumberOfElements(self, edition="FC26"):
        """Retourne le nombre de joueurs"""
        pass

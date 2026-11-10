
class ClubDAOInterface:
    """Interface pour le DAO Club"""

    def findAll(self):
        """Trouve tous les clubs"""
        pass

    def findById(self, club_id):
        """Trouve un club par son ID"""
        pass

    def findByNameSubword(self, name):
        """Recherche les clubs par nom"""
        pass

    def findByLeague(self, league_id):
        """Trouve les clubs d'un championnat"""
        pass

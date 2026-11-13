from app.models.ReferenceDAO import ReferenceSqliteDAO


class ReferenceService:
    """
    Service gérant les données de référence (championnats, postes, nationalités, playstyles).
    Fournit les listes nécessaires aux filtres et formulaires de l'application.
    """

    def __init__(self, reference_dao=None):
        self.reference_dao = reference_dao or ReferenceSqliteDAO()

    def get_positions(self):
        """Retourne la liste ordonnée des postes disponibles"""
        try:
            positions = self.reference_dao.getUniquePositions()
            if positions:
                return positions
        except Exception:
            pass
        return ['ST', 'RW', 'LW', 'CAM', 'CM', 'CDM', 'CB', 'LB', 'RB', 'GK', 'LM', 'RM']

    def get_leagues(self):
        """Retourne la liste ordonnée des championnats"""
        try:
            leagues = self.reference_dao.getUniqueLeagues()
            if leagues:
                # Filtrer les inconnus et renvoyer
                return [l for l in leagues if l and l != 'Unknown']
        except Exception:
            pass
        return ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Saudi Pro League', 'Major League Soccer']

    def get_countries(self):
        """Retourne la liste des nationalités"""
        try:
            countries = self.reference_dao.getUniqueCountries()
            if countries:
                return [c for c in countries if c and c != 'Unknown']
        except Exception:
            pass
        return ['France', 'Angleterre', 'Espagne', 'Brésil', 'Allemagne', 'Argentine', 'Uruguay', 'Portugal']

    def get_playstyles(self):
        """Retourne la liste des PlayStyles disponibles"""
        try:
            playstyles = self.reference_dao.getUniquePlaystyles()
            if playstyles:
                return playstyles
        except Exception:
            pass
        return [
            'Anticipate', 'Relentless', 'Quick Step', 'Rapid', 
            'Finesse Shot', 'Power Shot', 'Whipped Pass', 'Technical'
        ]

    def get_editions(self):
        """Retourne les éditions du jeu enregistrées"""
        try:
            return self.reference_dao.getUniqueEditions()
        except Exception:
            return ['FC26']

import os
import sqlite3
from typing import List, Optional
from app.models.player_model import Player, PlayerFilter
from app.database import init_db, get_db
from app.config import Config


class PlayerRepository:
    """
    Repository de gestion des données des joueurs FIFA / EA Sports FC.
    Communique directement avec la base de données SQLite via des requêtes SQL
    exécutées par le modèle Player (Architecture MVC classique).
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or Config.DATABASE_PATH
        # Vérification et initialisation automatique de la base SQLite si nécessaire
        self._ensure_database_ready()

    def _ensure_database_ready(self):
        """Vérifie si la base SQLite existe et contient des joueurs."""
        try:
            conn = get_db(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
            table_exists = cursor.fetchone()
            if not table_exists:
                init_db(self.db_path)
            else:
                cursor.execute("SELECT COUNT(*) FROM players")
                if cursor.fetchone()[0] == 0:
                    init_db(self.db_path)
        except Exception as e:
            # En cas d'erreur, tenter l'initialisation complète
            init_db(self.db_path)

    @property
    def players(self) -> List[Player]:
        """Propriété rétrocompatible : retourne les joueurs principaux ordonnés par note."""
        return self.get_all(limit=500)

    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Player]:
        """
        Requête SQL : Récupère la liste des joueurs ordonnés par note globale (overall).
        """
        return Player.find_all(limit=limit, offset=offset)

    def get_by_id(self, player_id: int) -> Optional[Player]:
        """
        Requête SQL : Récupère un joueur spécifique par sa clé primaire.
        """
        return Player.find_by_id(player_id)

    def count(self, position: Optional[str] = None, search: Optional[str] = None) -> int:
        """
        Requête SQL : COUNT(*) sur les joueurs selon critères.
        """
        return Player.count(position=position, search=search)

    def find_all(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        position: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Player]:
        """
        Requête SQL avec pagination, recherche textuelle et filtrage par poste.
        """
        return Player.find_all(limit=limit, offset=offset, position=position, search=search)

    def get_candidates(self, player_filter: PlayerFilter, limit: Optional[int] = None) -> List[Player]:
        """
        Requête SQL optimisée : Extrait les joueurs éligibles en filtrant dans SQLite
        sur le prix, le mauvais pied et le poste avant d'alimenter les algorithmes de recommandation.
        """
        return Player.find_candidates(player_filter=player_filter, limit=limit)

    def get_unique_clubs(self) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT club FROM players ...
        """
        return Player.get_unique_clubs()

    def get_unique_nationalities(self) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT nationality FROM players ...
        """
        return Player.get_unique_nationalities()

    def get_unique_leagues(self) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT league FROM players ...
        """
        return Player.get_unique_leagues()


# Instance singleton du repository
player_repository = PlayerRepository()

"""
Module des contrôleurs.
Exporte les Blueprints de l'application pour une utilisation modulaire.
"""

from app.blueprints import index_bp, scout_bp, compare_bp, pitch_bp, player_bp

__all__ = [
    "index_bp",
    "scout_bp",
    "compare_bp",
    "pitch_bp",
    "player_bp"
]

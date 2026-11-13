"""
Enregistrement centralisé des Blueprints / Contrôleurs de PickXI.
Chaque Blueprint isole une fonctionnalité avec ses routes et son contrôleur dédié.
"""

from .index import index_bp
from .scout import scout_bp
from .compare import compare_bp
from .pitch import pitch_bp
from .player import player_bp

__all__ = [
    "index_bp",
    "scout_bp",
    "compare_bp",
    "pitch_bp",
    "player_bp"
]

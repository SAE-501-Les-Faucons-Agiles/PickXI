"""
Package des services métiers de PickXI.
Encapsule la logique applicative, le scoring et les interactions avec les DAO.
"""

from app.services.PlayerService import PlayerService
from app.services.CompareService import CompareService
from app.services.PitchService import PitchService
from app.services.ReferenceService import ReferenceService

# Singletons partagés prêts à l'emploi
player_service = PlayerService()
compare_service = CompareService(player_service=player_service)
pitch_service = PitchService(player_service=player_service)
reference_service = ReferenceService()

__all__ = [
    "PlayerService",
    "CompareService",
    "PitchService",
    "ReferenceService",
    "player_service",
    "compare_service",
    "pitch_service",
    "reference_service"
]

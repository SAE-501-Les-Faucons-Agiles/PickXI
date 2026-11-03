from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Player:
    id: int
    name: str
    full_name: str
    overall: int
    position: str
    positions: List[str]
    club: str
    league: str
    nationality: str
    price: int  # En crédits FUT / valeur marchande
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physic: int
    weak_foot: int      # Mauvais pied (1-5 étoiles)
    skill_moves: int    # Gestes techniques (1-5 étoiles)
    image_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "overall": self.overall,
            "position": self.position,
            "positions": self.positions,
            "club": self.club,
            "league": self.league,
            "nationality": self.nationality,
            "price": self.price,
            "pace": self.pace,
            "shooting": self.shooting,
            "passing": self.passing,
            "dribbling": self.dribbling,
            "defending": self.defending,
            "physic": self.physic,
            "weak_foot": self.weak_foot,
            "skill_moves": self.skill_moves,
            "image_url": self.image_url
        }

@dataclass
class PlayerFilter:
    position: str = "ALL"
    max_price: int = 1_000_000
    min_weak_foot: int = 3
    target_club: str = ""
    target_league: str = ""
    target_nationality: str = ""
    # Poids accordés aux 6 stats fondamentales (entre 0.0 et 1.0)
    weight_pace: float = 1.0
    weight_shooting: float = 1.0
    weight_passing: float = 1.0
    weight_dribbling: float = 1.0
    weight_defending: float = 1.0
    weight_physic: float = 1.0

@dataclass
class PerformanceMetrics:
    execution_time_ms: float
    time_min_ms: float
    time_max_ms: float
    time_avg_ms: float
    theoretical_complexity: str
    space_complexity: str
    memory_usage_kb: float
    battery_impact_score: str
    comparison_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_time_ms": round(self.execution_time_ms, 3),
            "time_min_ms": round(self.time_min_ms, 3),
            "time_max_ms": round(self.time_max_ms, 3),
            "time_avg_ms": round(self.time_avg_ms, 3),
            "theoretical_complexity": self.theoretical_complexity,
            "space_complexity": self.space_complexity,
            "memory_usage_kb": round(self.memory_usage_kb, 2),
            "battery_impact_score": self.battery_impact_score,
            "comparison_notes": self.comparison_notes
        }

@dataclass
class RankedPlayer:
    player: Player
    score: float
    chemistry_points: int
    match_percentage: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "player": self.player.to_dict(),
            "score": round(self.score, 3),
            "chemistry_points": self.chemistry_points,
            "match_percentage": self.match_percentage
        }

@dataclass
class RecommendationResult:
    approach_id: str
    approach_name: str
    approach_description: str
    ranked_players: List[RankedPlayer]
    metrics: PerformanceMetrics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "approach_id": self.approach_id,
            "approach_name": self.approach_name,
            "approach_description": self.approach_description,
            "ranked_players": [rp.to_dict() for rp in self.ranked_players],
            "metrics": self.metrics.to_dict()
        }

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Item:
    id: int
    title: str
    category: str
    tags: List[str]
    rating: float
    popularity: int
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "tags": self.tags,
            "rating": self.rating,
            "popularity": self.popularity,
            "description": self.description
        }

@dataclass
class PerformanceMetrics:
    execution_time_ms: float
    time_min_ms: float
    time_max_ms: float
    time_avg_ms: float
    theoretical_complexity: str
    space_complexity: str
    memory_usage_kb: float
    battery_impact_score: str  # 'Très faible', 'Faible', 'Moyen', 'Élevé'
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
class RecommendationResult:
    approach_id: str
    approach_name: str
    approach_description: str
    items: List[Item]
    metrics: PerformanceMetrics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "approach_id": self.approach_id,
            "approach_name": self.approach_name,
            "approach_description": self.approach_description,
            "items": [item.to_dict() for item in self.items],
            "metrics": self.metrics.to_dict()
        }

from pydantic import BaseModel,Field
from typing import Literal

class RecommendationCriteria(BaseModel):
    position: Literal[
        "ST", "CB", "GK", "CM", "CAM", "CDM",
        "LW", "RW", "LM", "RM", "LB", "RB"
    ] | None = None

    qualites: list[
        Literal[
            "vitesse", "tir", "passe",
            "dribble", "défense", "physique"
        ]
    ] = Field(default_factory=list)  


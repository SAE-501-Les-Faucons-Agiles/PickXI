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

    max_age: int | None = Field(default=None, ge=15, le=50)
    min_age: int | None = Field(default=None, ge=15, le=50)
    max_budget: int | None = Field(default=None, ge=0)
    min_budget: int | None = Field(default=None, ge=0)


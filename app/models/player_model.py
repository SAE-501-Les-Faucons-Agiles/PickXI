import sqlite3
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from app.database import get_db

# Dictionnaire de correspondance des postes (Français <-> Anglais / Codes FUT SoFIFA)
POSITION_EQUIVALENTS: Dict[str, List[str]] = {
    "BU": ["ST", "CF", "BU"],
    "ST": ["ST", "CF", "BU"],
    "CF": ["CF", "ST", "BU"],
    "AG": ["LW", "LM", "AG"],
    "LW": ["LW", "LM", "AG"],
    "AD": ["RW", "RM", "AD"],
    "RW": ["RW", "RM", "AD"],
    "MOC": ["CAM", "MOC"],
    "CAM": ["CAM", "MOC"],
    "MC": ["CM", "MC"],
    "CM": ["CM", "MC"],
    "MDC": ["CDM", "MDC"],
    "CDM": ["CDM", "MDC"],
    "DC": ["CB", "DC"],
    "CB": ["CB", "DC"],
    "DG": ["LB", "LWB", "DG"],
    "LB": ["LB", "LWB", "DG"],
    "LWB": ["LWB", "LB", "DG"],
    "DD": ["RB", "RWB", "DD"],
    "RB": ["RB", "RWB", "DD"],
    "RWB": ["RWB", "RB", "DD"],
    "MG": ["LM", "MG"],
    "LM": ["LM", "MG"],
    "MD": ["RM", "MD"],
    "RM": ["RM", "MD"],
    "G": ["GK", "G"],
    "GK": ["GK", "G"]
}


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

    @classmethod
    def from_row(cls, row: Any) -> "Player":
        """Instancie un Player depuis un sqlite3.Row ou un tuple/dict."""
        raw_pos = row["positions"] if "positions" in row.keys() else row["position"]
        pos_list = [p.strip().upper() for p in raw_pos.split(",") if p.strip()]

        return cls(
            id=int(row["id"]),
            name=row["name"],
            full_name=row["full_name"],
            overall=int(row["overall"]),
            position=row["position"],
            positions=pos_list,
            club=row["club"],
            league=row["league"],
            nationality=row["nationality"],
            price=int(row["price"]),
            pace=int(row["pace"]),
            shooting=int(row["shooting"]),
            passing=int(row["passing"]),
            dribbling=int(row["dribbling"]),
            defending=int(row["defending"]),
            physic=int(row["physic"]),
            weak_foot=int(row["weak_foot"]),
            skill_moves=int(row["skill_moves"]),
            image_url=row["image_url"] or ""
        )

    # -------------------------------------------------------------
    # Requêtes SQL classiques sur la base de données SQLite
    # -------------------------------------------------------------

    @classmethod
    def find_by_id(cls, player_id: int, conn: Optional[sqlite3.Connection] = None) -> Optional["Player"]:
        """
        Requête SQL pour récupérer un joueur par son ID.
        SELECT * FROM players WHERE id = ?
        """
        db = conn or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
        row = cursor.fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def find_all(
        cls,
        limit: Optional[int] = None,
        offset: int = 0,
        position: Optional[str] = None,
        search: Optional[str] = None,
        conn: Optional[sqlite3.Connection] = None
    ) -> List["Player"]:
        """
        Requête SQL pour lister les joueurs avec pagination, filtrage par poste et recherche.
        """
        db = conn or get_db()
        cursor = db.cursor()

        query_parts = ["SELECT * FROM players"]
        where_clauses = []
        params: List[Any] = []

        if search:
            search_param = f"%{search.strip()}%"
            where_clauses.append("(name LIKE ? OR full_name LIKE ? OR club LIKE ?)")
            params.extend([search_param, search_param, search_param])

        if position and position != "ALL":
            targets = POSITION_EQUIVALENTS.get(position.upper(), [position.upper()])
            placeholders = ", ".join("?" for _ in targets)
            like_clauses = " OR ".join("positions LIKE ?" for _ in targets)
            where_clauses.append(f"(position IN ({placeholders}) OR {like_clauses})")
            params.extend(targets)
            params.extend([f"%{t}%" for t in targets])

        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))

        query_parts.append("ORDER BY overall DESC, price ASC")

        if limit is not None:
            query_parts.append("LIMIT ? OFFSET ?")
            params.extend([limit, offset])

        sql = " ".join(query_parts)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def count(
        cls,
        position: Optional[str] = None,
        search: Optional[str] = None,
        conn: Optional[sqlite3.Connection] = None
    ) -> int:
        """
        Requête SQL COUNT(*) pour connaître le total de joueurs correspondant à un filtre.
        """
        db = conn or get_db()
        cursor = db.cursor()

        query_parts = ["SELECT COUNT(*) FROM players"]
        where_clauses = []
        params: List[Any] = []

        if search:
            search_param = f"%{search.strip()}%"
            where_clauses.append("(name LIKE ? OR full_name LIKE ? OR club LIKE ?)")
            params.extend([search_param, search_param, search_param])

        if position and position != "ALL":
            targets = POSITION_EQUIVALENTS.get(position.upper(), [position.upper()])
            placeholders = ", ".join("?" for _ in targets)
            like_clauses = " OR ".join("positions LIKE ?" for _ in targets)
            where_clauses.append(f"(position IN ({placeholders}) OR {like_clauses})")
            params.extend(targets)
            params.extend([f"%{t}%" for t in targets])

        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))

        sql = " ".join(query_parts)
        cursor.execute(sql, params)
        return cursor.fetchone()[0]

    @classmethod
    def find_candidates(
        cls,
        player_filter: "PlayerFilter",
        limit: Optional[int] = None,
        conn: Optional[sqlite3.Connection] = None
    ) -> List["Player"]:
        """
        Requête SQL ciblée pour extraire les joueurs candidats aux algorithmes de recommandation.
        Filtre en amont dans SQLite via les index (prix, mauvais pied, poste).
        """
        db = conn or get_db()
        cursor = db.cursor()

        where_clauses = [
            "price <= ?",
            "weak_foot >= ?"
        ]
        params: List[Any] = [player_filter.max_price, player_filter.min_weak_foot]

        # Filtre sur le poste (avec gestion des équivalents FR/EN comme BU <-> ST)
        if player_filter.position and player_filter.position != "ALL":
            targets = POSITION_EQUIVALENTS.get(player_filter.position.upper(), [player_filter.position.upper()])
            placeholders = ", ".join("?" for _ in targets)
            like_clauses = " OR ".join("positions LIKE ?" for _ in targets)
            where_clauses.append(f"(position IN ({placeholders}) OR {like_clauses})")
            params.extend(targets)
            params.extend([f"%{t}%" for t in targets])

        sql = f"SELECT * FROM players WHERE {' AND '.join(where_clauses)} ORDER BY overall DESC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def get_unique_clubs(cls, conn: Optional[sqlite3.Connection] = None) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT club FROM players ...
        """
        db = conn or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT club FROM players WHERE club != '' AND club IS NOT NULL ORDER BY club ASC")
        return [row[0] for row in cursor.fetchall()]

    @classmethod
    def get_unique_leagues(cls, conn: Optional[sqlite3.Connection] = None) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT league FROM players ...
        """
        db = conn or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT league FROM players WHERE league != '' AND league IS NOT NULL ORDER BY league ASC")
        return [row[0] for row in cursor.fetchall()]

    @classmethod
    def get_unique_nationalities(cls, conn: Optional[sqlite3.Connection] = None) -> List[str]:
        """
        Requête SQL : SELECT DISTINCT nationality FROM players ...
        """
        db = conn or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT nationality FROM players WHERE nationality != '' AND nationality IS NOT NULL ORDER BY nationality ASC")
        return [row[0] for row in cursor.fetchall()]


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

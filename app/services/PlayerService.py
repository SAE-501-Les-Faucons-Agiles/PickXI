import math
from app.models.PlayerDAO import PlayerSqliteDAO
from app.models.PlayerStatsDAO import PlayerStatsSqliteDAO
from app.services.ScoringService import ScoringService

class PlayerService:
    """
    Service métier responsable de la recherche, détection,
    formatage et recommandation des joueurs FC 26.
    """

    def __init__(self, player_dao=None, stats_dao=None):
        self.player_dao = player_dao or PlayerSqliteDAO()
        self.stats_dao = stats_dao or PlayerStatsSqliteDAO()

    def _build_face_url(self, sofifa_id):
        """Génère l'URL officielle de la photo du joueur sur SoFIFA"""
        if not sofifa_id:
            return "/static/img/logo.png"
        sid_str = str(sofifa_id).zfill(6)
        part1 = sid_str[:3]
        part2 = sid_str[3:]
        return f"https://cdn.sofifa.net/players/{part1}/{part2}/26_120.png"

    def _format_player(self, player, stats=None):
        """Convertit un objet Player en dictionnaire complet avec métadonnées UI"""
        if not player:
            return None

        # Si c'est déjà un dictionnaire
        if isinstance(player, dict):
            d = dict(player)
        else:
            d = {
                "sofifa_id": player.sofifa_id,
                "name": player.name,
                "birth_date": getattr(player, "birth_date", "2000-01-01"),
                "nationality": getattr(player, "nationality", "France"),
                "edition": getattr(player, "edition", "FC26"),
                "club": getattr(player, "club", "Club"),
                "age": getattr(player, "age", 25),
                "position": getattr(player, "position", "ST"),
                "overall": getattr(player, "overall", 80),
                "potential": getattr(player, "potential", 82),
                "pace": getattr(player, "pace", 75),
                "shooting": getattr(player, "shooting", 75),
                "passing": getattr(player, "passing", 75),
                "dribbling": getattr(player, "dribbling", 75),
                "defending": getattr(player, "defending", 75),
                "physicality": getattr(player, "physicality", 75),
                "market_value_eur": getattr(player, "market_value_eur", 20000000),
                "weak_foot": getattr(player, "weak_foot", 3),
                "skill_moves": getattr(player, "skill_moves", 3),
                "player_traits": getattr(player, "player_traits", ""),
            }

        # URL Photo SoFIFA
        if not d.get("face_url"):
            d["face_url"] = self._build_face_url(d["sofifa_id"])

        # Playstyles par défaut ou calculés
        if not d.get("playstyles"):
            ovr = d.get("overall", 80)
            pos = d.get("position", "CM")
            if pos in ["ST", "RW", "LW", "CF"]:
                d["playstyles"] = [{"name": "Finesse Shot", "is_plus": ovr >= 88}]
            elif pos in ["CB", "LB", "RB", "LWB", "RWB"]:
                d["playstyles"] = [{"name": "Anticipate", "is_plus": ovr >= 88}]
            elif pos in ["CDM", "CM", "CAM"]:
                d["playstyles"] = [{"name": "Relentless", "is_plus": ovr >= 88}]
            else:
                d["playstyles"] = [{"name": "Far Throw", "is_plus": False}]

        return d

    def get_curated_players(self, limit=4):
        """Retourne une sélection de joueurs phares pour la page d'accueil"""
        featured_ids = [252371, 239053, 235212, 231866] # Bellingham, Valverde, Hakimi, Rodri
        curated = []

        for fid in featured_ids:
            try:
                p = self.player_dao.findById(fid)
                if p:
                    curated.append(self._format_player(p))
            except Exception:
                pass

        if len(curated) < limit:
            try:
                all_players = self.player_dao.findAll()
                for p in all_players[:limit]:
                    if p.sofifa_id not in [x["sofifa_id"] for x in curated]:
                        curated.append(self._format_player(p))
                        if len(curated) >= limit:
                            break
            except Exception:
                pass

        # Fallback de sécurité si BD non chargée
        if not curated:
            curated = [
                {
                    "sofifa_id": 252371, "name": "J. Bellingham", "overall": 90, "position": "CAM",
                    "club": "Real Madrid", "nationality": "Angleterre", "pace": 80, "shooting": 86,
                    "passing": 83, "dribbling": 90, "defending": 78, "physicality": 85,
                    "market_value_eur": 174500000, "face_url": self._build_face_url(252371),
                    "playstyles": [{"name": "Relentless", "is_plus": True}]
                },
                {
                    "sofifa_id": 239053, "name": "F. Valverde", "overall": 89, "position": "CM",
                    "club": "Real Madrid", "nationality": "Uruguay", "pace": 88, "shooting": 84,
                    "passing": 84, "dribbling": 84, "defending": 83, "physicality": 85,
                    "market_value_eur": 120500000, "face_url": self._build_face_url(239053),
                    "playstyles": [{"name": "Rapid", "is_plus": True}]
                },
                {
                    "sofifa_id": 235212, "name": "A. Hakimi", "overall": 89, "position": "RB",
                    "club": "Paris Saint-Germain", "nationality": "Maroc", "pace": 92, "shooting": 79,
                    "passing": 82, "dribbling": 83, "defending": 82, "physicality": 79,
                    "market_value_eur": 111000000, "face_url": self._build_face_url(235212),
                    "playstyles": [{"name": "Quick Step", "is_plus": True}]
                },
                {
                    "sofifa_id": 231866, "name": "Rodri", "overall": 90, "position": "CDM",
                    "club": "Manchester City", "nationality": "Espagne", "pace": 65, "shooting": 80,
                    "passing": 86, "dribbling": 84, "defending": 86, "physicality": 85,
                    "market_value_eur": 102000000, "face_url": self._build_face_url(231866),
                    "playstyles": [{"name": "Power Shot", "is_plus": True}]
                }
            ]

        return curated[:limit]

    def get_player_by_id(self, sofifa_id):
        """Récupère un joueur complet par son ID SoFIFA avec ses statistiques détaillées"""
        try:
            player = self.player_dao.findById(sofifa_id)
            if not player:
                return None
            
            p_dict = self._format_player(player)

            # Statistiques avancées depuis PlayerStatsDAO
            stats = None
            try:
                stats = self.stats_dao.findByPlayerId(sofifa_id)
            except Exception:
                pass

            return p_dict, stats
        except Exception:
            return None, None

    def search_players(self, filters, page=1, per_page=12):
        """
        Recherche par critères avec algorithme de scoring :
        1. Filtres stricts (barrages) : poste, budget max, âge max, pied fort, championnat, recherche texte.
        2. Calcul du match_score sur les stats cibles + bonus PlayStyle (+10).
        3. Tri par match_score décroissant puis overall décroissant (ou autre tri choisi).
        """
        def _to_int(val):
            try:
                return int(val) if val not in (None, "", "ALL") else None
            except (ValueError, TypeError):
                return None

        q = (filters.get("q") or "").strip()
        pos = filters.get("pos") or "ALL"
        max_age = _to_int(filters.get("max_age"))
        preferred_foot = (filters.get("preferred_foot") or "").strip()
        league = filters.get("league") or "ALL"
        playstyle = filters.get("playstyle") or "ALL"
        sort_mode = filters.get("sort") or "score_desc"

        # Traitement du budget (conversion M€ -> € si slider < 500, et 150 = illimité)
        raw_budget = _to_int(filters.get("max_budget"))
        if raw_budget is not None and raw_budget < 150:
            max_budget_eur = raw_budget * 1_000_000
        elif raw_budget is not None and raw_budget >= 500:
            max_budget_eur = raw_budget
        else:
            max_budget_eur = None

        # 1. Extraction des candidats via filtres stricts
        try:
            candidates = self.player_dao.findCandidatesForScoring(
                q=q or None,
                position=pos,
                max_budget=max_budget_eur,
                max_age=max_age if (max_age is not None and max_age < 38) else None,
                preferred_foot=preferred_foot or None,
                league=league,
                min_overall=_to_int(filters.get("min_ovr")),  # <-- Nouveau paramètre
            )
        except Exception as e:
            import traceback
            print("ERREUR SCORING DAO :", e)
            traceback.print_exc()
            candidates = []

        # 2. Construction des cibles de stats pour le scoring
        cibles_stats = {
            "overall": _to_int(filters.get("min_ovr")),
            "potential": _to_int(filters.get("min_potential")),
            "pace": _to_int(filters.get("min_pace")),
            "shooting": _to_int(filters.get("min_shooting")),
            "passing": _to_int(filters.get("min_passing")),
            "dribbling": _to_int(filters.get("min_dribbling")),
            "defending": _to_int(filters.get("min_defending")),
            "physicality": _to_int(filters.get("min_physicality")),
            "weak_foot": _to_int(filters.get("weak_foot")),
            "skill_moves": _to_int(filters.get("skill_moves")),
        }
        # On ne garde que les critères réellement renseignés
        cibles_stats = {k: v for k, v in cibles_stats.items() if v is not None}

        traits_souhaites = [playstyle] if playstyle and playstyle != "ALL" else []

        # 3. Calcul du score pour chaque candidat
        for joueur in candidates:
            if cibles_stats or traits_souhaites:
                joueur["match_score"] = ScoringService.calculer_score(
                    joueur, cibles_stats, traits_souhaites
                )
            else:
                joueur["match_score"] = None

        # 4. Tri
        if sort_mode == "pace_desc":
            candidates.sort(key=lambda x: (x.get("pace") or 0, x.get("overall") or 0), reverse=True)
        elif sort_mode == "price_asc":
            candidates.sort(key=lambda x: x.get("market_value_eur") if x.get("market_value_eur") is not None else float("inf"))
        elif sort_mode == "price_desc":
            candidates.sort(key=lambda x: x.get("market_value_eur") or 0, reverse=True)
        elif sort_mode == "potential_desc":
            candidates.sort(key=lambda x: (x.get("potential") or 0, x.get("overall") or 0), reverse=True)
        elif sort_mode == "overall_desc":
            candidates.sort(key=lambda x: x.get("overall") or 0, reverse=True)
        else:
            # score_desc par défaut : score décroissant, puis overall pour départager
            candidates.sort(
                key=lambda x: (
                    x.get("match_score") if x.get("match_score") is not None else -9999,
                    x.get("overall") or 0,
                ),
                reverse=True,
            )

        total_count = len(candidates)
        total_pages = max(1, math.ceil(total_count / per_page))
        current_page = max(1, min(page, total_pages))

        start_idx = (current_page - 1) * per_page
        end_idx = start_idx + per_page
        paged_list = [self._format_player(p) for p in candidates[start_idx:end_idx]]

        return {
            "players": paged_list,
            "total_count": total_count,
            "page": current_page,
            "total_pages": total_pages,
            "per_page": per_page,
        }
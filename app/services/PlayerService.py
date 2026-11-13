import math
from app.models.PlayerDAO import PlayerSqliteDAO
from app.models.PlayerStatsDAO import PlayerStatsSqliteDAO


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
        Recherche complète avec filtres multi-critères et pagination.
        filters = {
            'q': str, 'pos': str, 'min_ovr': int, 'min_pace': int,
            'max_budget': int (en M€ ou €), 'max_age': int, 'league': str,
            'playstyle': str, 'sort': str
        }
        """
        q = (filters.get("q") or "").strip().lower()
        pos = filters.get("pos") or "ALL"
        min_ovr = int(filters.get("min_ovr")) if filters.get("min_ovr") else None
        min_pace = int(filters.get("min_pace")) if filters.get("min_pace") else None
        max_age = int(filters.get("max_age")) if filters.get("max_age") else None
        max_budget = filters.get("max_budget")
        league = filters.get("league") or "ALL"
        sort_mode = filters.get("sort") or "overall_desc"

        # Traitement du budget (conversion en euros si exprimé en M€)
        if max_budget is not None and str(max_budget).isdigit():
            val = int(max_budget)
            if val < 500: # Valeur passée en M€ depuis le slider
                max_budget_eur = val * 1000000
            else:
                max_budget_eur = val
        else:
            max_budget_eur = None

        position_param = None if pos == "ALL" else pos

        try:
            # Si une recherche par nom est demandée
            if q:
                results = self.player_dao.findByNameSubword(q)
            else:
                results = self.player_dao.findByCriteria(
                    position=position_param,
                    min_overall=min_ovr,
                    max_age=max_age,
                    max_budget=max_budget_eur,
                    min_pace=min_pace
                )
        except Exception:
            results = []

        # Filtrage en mémoire supplémentaire si nécessaire (ex: ligue, q combiné)
        filtered = []
        for p in results:
            if position_param and getattr(p, "position", "") != position_param:
                continue
            if min_ovr and getattr(p, "overall", 0) < min_ovr:
                continue
            if min_pace and getattr(p, "pace", 0) < min_pace:
                continue
            if max_age and getattr(p, "age", 0) > max_age:
                continue
            if max_budget_eur and getattr(p, "market_value_eur", 0) > max_budget_eur:
                continue
            if league and league != "ALL":
                p_club = getattr(p, "club", "")
                # Si le club ou la ligue ne matche pas
                if hasattr(p, "league") and p.league and p.league != league:
                    continue

            filtered.append(p)

        # Tri
        if sort_mode == "pace_desc":
            filtered.sort(key=lambda x: getattr(x, "pace", 0) or 0, reverse=True)
        elif sort_mode == "price_asc":
            filtered.sort(key=lambda x: getattr(x, "market_value_eur", 0) or 0)
        elif sort_mode == "price_desc":
            filtered.sort(key=lambda x: getattr(x, "market_value_eur", 0) or 0, reverse=True)
        elif sort_mode == "potential_desc":
            filtered.sort(key=lambda x: getattr(x, "potential", 0) or 0, reverse=True)
        else:
            # overall_desc par défaut
            filtered.sort(key=lambda x: getattr(x, "overall", 0) or 0, reverse=True)

        total_count = len(filtered)
        total_pages = max(1, math.ceil(total_count / per_page))
        current_page = max(1, min(page, total_pages))

        start_idx = (current_page - 1) * per_page
        end_idx = start_idx + per_page
        paged_list = [self._format_player(p) for p in filtered[start_idx:end_idx]]

        return {
            "players": paged_list,
            "total_count": total_count,
            "page": current_page,
            "total_pages": total_pages,
            "per_page": per_page
        }

    def get_similar_players(self, player, limit=4):
        """Trouve des joueurs similaires en poste et niveau général"""
        if not player:
            return []
        
        pos = player.get("position") if isinstance(player, dict) else getattr(player, "position", "CM")
        ovr = player.get("overall") if isinstance(player, dict) else getattr(player, "overall", 80)
        current_id = player.get("sofifa_id") if isinstance(player, dict) else getattr(player, "sofifa_id", 0)

        try:
            candidates = self.player_dao.findByCriteria(
                position=pos,
                min_overall=max(70, ovr - 4)
            )
            similar = []
            for c in candidates:
                if c.sofifa_id != current_id:
                    similar.append(self._format_player(c))
                    if len(similar) >= limit:
                        break
            return similar
        except Exception:
            return []

    def get_total_count(self):
        """Retourne le nombre total de joueurs enregistrés"""
        try:
            return self.player_dao.getNumberOfElements()
        except Exception:
            return 18405

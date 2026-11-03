import os
import csv
import glob
from typing import List, Dict, Set, Optional
from app.models.player_model import Player

# Dataset de base prêt à l'emploi (Top cartes EA Sports FC 25 / 26)
DEFAULT_PLAYERS: List[Player] = [
    Player(1, "K. Mbappé", "Kylian Mbappé", 91, "BU", ["BU", "AG"], "Real Madrid", "LaLiga", "France", 2800000, 97, 90, 80, 92, 36, 78, 4, 5),
    Player(2, "E. Haaland", "Erling Haaland", 91, "BU", ["BU"], "Manchester City", "Premier League", "Norvège", 2400000, 88, 92, 70, 81, 45, 88, 3, 3),
    Player(3, "Vinícius Jr.", "Vinícius José Paixão de Oliveira Júnior", 90, "AG", ["AG", "BU"], "Real Madrid", "LaLiga", "Brésil", 2100000, 95, 84, 81, 91, 29, 69, 4, 5),
    Player(4, "J. Bellingham", "Jude Bellingham", 90, "MOC", ["MOC", "MC"], "Real Madrid", "LaLiga", "Angleterre", 1900000, 80, 87, 83, 88, 78, 83, 4, 4),
    Player(5, "Rodri", "Rodrigo Hernández Cascante", 91, "MDC", ["MDC", "MC"], "Manchester City", "Premier League", "Espagne", 1500000, 66, 80, 86, 84, 87, 85, 4, 3),
    Player(6, "K. De Bruyne", "Kevin De Bruyne", 90, "MC", ["MC", "MOC"], "Manchester City", "Premier League", "Belgique", 950000, 67, 87, 94, 87, 65, 75, 5, 4),
    Player(7, "M. Salah", "Mohamed Salah", 89, "AD", ["AD", "BU"], "Liverpool", "Premier League", "Égypte", 850000, 89, 87, 82, 88, 45, 76, 3, 4),
    Player(8, "V. van Dijk", "Virgil van Dijk", 89, "DC", ["DC"], "Liverpool", "Premier League", "Pays-Bas", 1100000, 78, 60, 72, 72, 89, 86, 3, 2),
    Player(9, "W. Saliba", "William Saliba", 87, "DC", ["DC"], "Arsenal", "Premier League", "France", 450000, 82, 39, 69, 72, 87, 82, 3, 2),
    Player(10, "B. Saka", "Bukayo Saka", 87, "AD", ["AD", "MD"], "Arsenal", "Premier League", "Angleterre", 380000, 86, 83, 83, 87, 65, 76, 3, 4),
    Player(11, "J. Musiala", "Jamal Musiala", 87, "MOC", ["MOC", "MC", "AG"], "Bayern Munich", "Bundesliga", "Allemagne", 600000, 85, 82, 81, 90, 64, 63, 4, 5),
    Player(12, "F. Wirtz", "Florian Wirtz", 88, "MOC", ["MOC", "MC"], "Bayer Leverkusen", "Bundesliga", "Allemagne", 700000, 81, 81, 87, 89, 53, 68, 4, 4),
    Player(13, "E. Camavinga", "Eduardo Camavinga", 83, "MDC", ["MDC", "MC", "DG"], "Real Madrid", "LaLiga", "France", 85000, 81, 66, 80, 82, 80, 81, 3, 4),
    Player(14, "F. Valverde", "Federico Valverde", 88, "MC", ["MC", "MD"], "Real Madrid", "LaLiga", "Uruguay", 850000, 88, 82, 84, 84, 80, 84, 4, 3),
    Player(15, "T. Hernández", "Theo Hernández", 87, "DG", ["DG"], "AC Milan", "Serie A", "France", 520000, 95, 73, 76, 84, 80, 89, 3, 3),
    Player(16, "A. Davies", "Alphonso Davies", 82, "DG", ["DG", "MG"], "Bayern Munich", "Bundesliga", "Canada", 95000, 95, 68, 77, 84, 74, 76, 4, 4),
    Player(17, "A. Hakimi", "Achraf Hakimi", 84, "DD", ["DD", "MD"], "Paris Saint-Germain", "Ligue 1", "Maroc", 120000, 92, 75, 79, 80, 75, 78, 4, 4),
    Player(18, "O. Dembélé", "Ousmane Dembélé", 86, "AD", ["AD", "AG"], "Paris Saint-Germain", "Ligue 1", "France", 310000, 93, 77, 81, 87, 36, 56, 5, 5),
    Player(19, "A. Griezmann", "Antoine Griezmann", 88, "BU", ["BU", "MOC"], "Atlético Madrid", "LaLiga", "France", 420000, 80, 88, 86, 87, 72, 73, 4, 4),
    Player(20, "H. Kane", "Harry Kane", 90, "BU", ["BU"], "Bayern Munich", "Bundesliga", "Angleterre", 650000, 65, 93, 84, 83, 49, 82, 5, 3),
    Player(21, "J. Koundé", "Jules Koundé", 85, "DC", ["DC", "DD"], "FC Barcelone", "LaLiga", "France", 220000, 84, 45, 65, 73, 86, 78, 3, 3),
    Player(22, "Pedri", "Pedro González López", 86, "MC", ["MC"], "FC Barcelone", "LaLiga", "Espagne", 310000, 78, 67, 84, 88, 68, 73, 4, 4),
    Player(23, "L. Yamal", "Lamine Yamal Nasraoui Ebana", 81, "AD", ["AD"], "FC Barcelone", "LaLiga", "Espagne", 180000, 85, 74, 77, 84, 32, 50, 3, 4),
    Player(24, "R. Leão", "Rafael Alexandre da Conceição Leão", 86, "AG", ["AG", "BU"], "AC Milan", "Serie A", "Portugal", 340000, 93, 81, 76, 87, 28, 76, 4, 5),
    Player(25, "G. Donnarumma", "Gianluigi Donnarumma", 89, "G", ["G"], "Paris Saint-Germain", "Ligue 1", "Italie", 480000, 89, 85, 79, 90, 52, 85, 3, 1),
    Player(26, "T. Courtois", "Thibaut Courtois", 89, "G", ["G"], "Real Madrid", "LaLiga", "Belgique", 510000, 85, 89, 76, 88, 46, 88, 3, 1)
]

class PlayerRepository:
    """
    Gestionnaire de données des joueurs FIFA / EA Sports FC.
    Capable de charger automatiquement le CSV Kaggle (SoFIFA)
    ou de basculer sur le dataset de référence par défaut.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.players: List[Player] = []
        self._load_data()

    def _load_data(self):
        # Recherche de fichiers CSV dans le dossier data/
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))
        loaded = False

        if csv_files:
            target_csv = csv_files[0]
            try:
                self.players = self._parse_kaggle_csv(target_csv)
                if len(self.players) > 0:
                    print(f"✅ {len(self.players)} joueurs chargés depuis le CSV Kaggle: {target_csv}")
                    loaded = True
            except Exception as e:
                print(f"⚠️ Erreur lors du parsing du CSV ({e}), utilisation des données de secours.")

        if not loaded:
            self.players = list(DEFAULT_PLAYERS)
            print(f"ℹ️ {len(self.players)} joueurs de référence chargés (Base FC 25/26).")

    def _parse_kaggle_csv(self, file_path: str) -> List[Player]:
        players: List[Player] = []
        with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            idx = 1
            for row in reader:
                try:
                    name = row.get("short_name") or row.get("name") or f"Joueur {idx}"
                    full_name = row.get("long_name") or name
                    overall = int(float(row.get("overall", row.get("overall_rating", 75))))
                    
                    # Positions
                    raw_pos = row.get("player_positions") or row.get("position") or "BU"
                    positions = [p.strip().upper() for p in raw_pos.split(",")]
                    main_pos = positions[0] if positions else "BU"

                    club = row.get("club_name") or "Club Libre"
                    league = row.get("league_name") or "Ligue Internationale"
                    nationality = row.get("nationality_name") or "Monde"

                    # Prix / Valeur marchande en crédits
                    raw_val = row.get("value_eur") or "100000"
                    try:
                        price = int(float(raw_val))
                    except ValueError:
                        price = 150000

                    # 6 Stats clés
                    pace = int(float(row.get("pace", row.get("movement_sprint_speed", 70) or 70)))
                    shooting = int(float(row.get("shooting", row.get("attacking_finishing", 70) or 70)))
                    passing = int(float(row.get("passing", row.get("skill_long_passing", 70) or 70)))
                    dribbling = int(float(row.get("dribbling", row.get("skill_dribbling", 70) or 70)))
                    defending = int(float(row.get("defending", row.get("defending_standing_tackle", 60) or 60)))
                    physic = int(float(row.get("physic", row.get("power_strength", 70) or 70)))

                    weak_foot = int(float(row.get("weak_foot", 3) or 3))
                    skill_moves = int(float(row.get("skill_moves", 3) or 3))
                    img = row.get("player_face_url") or row.get("image_url") or ""

                    players.append(Player(
                        id=idx,
                        name=name,
                        full_name=full_name,
                        overall=overall,
                        position=main_pos,
                        positions=positions,
                        club=club,
                        league=league,
                        nationality=nationality,
                        price=price,
                        pace=pace,
                        shooting=shooting,
                        passing=passing,
                        dribbling=dribbling,
                        defending=defending,
                        physic=physic,
                        weak_foot=weak_foot,
                        skill_moves=skill_moves,
                        image_url=img
                    ))
                    idx += 1
                except Exception:
                    continue
        return players

    def get_all(self) -> List[Player]:
        return self.players

    def get_by_id(self, player_id: int) -> Optional[Player]:
        for p in self.players:
            if p.id == player_id:
                return p
        return None

    def get_unique_clubs(self) -> List[str]:
        return sorted(list(set(p.club for p in self.players if p.club)))

    def get_unique_nationalities(self) -> List[str]:
        return sorted(list(set(p.nationality for p in self.players if p.nationality)))

    def get_unique_leagues(self) -> List[str]:
        return sorted(list(set(p.league for p in self.players if p.league)))

player_repository = PlayerRepository()

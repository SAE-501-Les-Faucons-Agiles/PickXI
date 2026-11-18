
class Player:

    def __init__(self, dico):
        self.sofifa_id = dico["sofifa_id"]
        self.name = dico["name"]
        self.birth_date = dico["birth_date"]
        self.nationality = dico["nationality"]

        self.edition = dico["edition"]
        self.club = dico["club"]
        self.age = dico["age"]
        self.position = dico["position"]

        self.overall = dico["overall"]
        self.potential = dico["potential"]

        self.pace = dico["pace"]
        self.shooting = dico["shooting"]
        self.passing = dico["passing"]
        self.dribbling = dico["dribbling"]
        self.defending = dico["defending"]
        self.physicality = dico["physicality"]

        self.market_value_eur = dico["market_value_eur"]
        self.market_value_date = dico["market_value_date"]

        self.weak_foot = dico.get("weak_foot")
        self.skill_moves = dico.get("skill_moves")
        self.player_traits = dico.get("player_traits")

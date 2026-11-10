
class MarketValue:

    def __init__(self, dico):
        self.tm_player_id = dico["tm_player_id"]
        self.name = dico["name"]
        self.value_eur = dico["value_eur"]
        self.valuation_date = dico["valuation_date"]
        self.method = dico["method"]

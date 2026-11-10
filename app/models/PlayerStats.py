
class PlayerStats:

    def __init__(self, dico):
        self.player_edition_id = dico["player_edition_id"]
        self.sofifa_id = dico["sofifa_id"]
        self.name = dico["name"]
        self.edition = dico["edition"]

        self.overall = dico["overall"]
        self.potential = dico["potential"]

        self.pace = dico["pace"]
        self.shooting = dico["shooting"]
        self.passing = dico["passing"]
        self.dribbling = dico["dribbling"]
        self.defending = dico["defending"]
        self.physicality = dico["physicality"]

        self.attacking_finishing = dico["attacking_finishing"]
        self.attacking_crossing = dico["attacking_crossing"]
        self.attacking_short_passing = dico["attacking_short_passing"]

        self.skill_ball_control = dico["skill_ball_control"]
        self.skill_dribbling = dico["skill_dribbling"]

        self.movement_acceleration = dico["movement_acceleration"]
        self.movement_sprint_speed = dico["movement_sprint_speed"]
        self.movement_agility = dico["movement_agility"]

        self.power_stamina = dico["power_stamina"]
        self.power_strength = dico["power_strength"]

        self.mentality_vision = dico["mentality_vision"]
        self.mentality_composure = dico["mentality_composure"]

        self.defending_standing_tackle = dico["defending_standing_tackle"]
        self.defending_sliding_tackle = dico["defending_sliding_tackle"]

        self.goalkeeping_diving = dico["goalkeeping_diving"]
        self.goalkeeping_handling = dico["goalkeeping_handling"]
        self.goalkeeping_kicking = dico["goalkeeping_kicking"]
        self.goalkeeping_positioning = dico["goalkeeping_positioning"]
        self.goalkeeping_reflexes = dico["goalkeeping_reflexes"]

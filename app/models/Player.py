from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Player(Base):
    """
    Modèle ORM représentant un joueur dans une édition du jeu.
    Mappé sur la vue SQLite v_recommendations.
    """
    __tablename__ = "v_recommendations"

    sofifa_id = Column(Integer, primary_key=True)
    edition = Column(String, primary_key=True)
    name = Column(String)
    birth_date = Column(String)
    nationality = Column(String)
    club = Column(String)
    overall = Column(Integer)
    potential = Column(Integer)
    age = Column(Integer)
    position = Column(String)
    pace = Column(Integer)
    shooting = Column(Integer)
    passing = Column(Integer)
    dribbling = Column(Integer)
    defending = Column(Integer)
    physicality = Column(Integer)
    market_value_eur = Column(Integer)
    market_value_date = Column(String)

    def __init__(self, dico=None, **kwargs):
        if dico and isinstance(dico, dict):
            for key, value in dico.items():
                setattr(self, key, value)
        else:
            super().__init__(**kwargs)

    def __getitem__(self, item):
        return getattr(self, item)

    def to_dict(self):
        """Convertit l'instance ORM en dictionnaire"""
        return {
            "sofifa_id": self.sofifa_id,
            "name": self.name,
            "birth_date": self.birth_date,
            "nationality": self.nationality,
            "edition": self.edition,
            "club": self.club,
            "overall": self.overall,
            "potential": self.potential,
            "age": self.age,
            "position": self.position,
            "pace": self.pace,
            "shooting": self.shooting,
            "passing": self.passing,
            "dribbling": self.dribbling,
            "defending": self.defending,
            "physicality": self.physicality,
            "market_value_eur": self.market_value_eur,
            "market_value_date": self.market_value_date
        }

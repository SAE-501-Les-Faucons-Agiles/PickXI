from app.database.db import get_session
from app.models.Player import Player
from app.models.PlayerDAOInterface import PlayerDAOInterface


class PlayerSqliteDAO(PlayerDAOInterface):
    """
    Player data access object dédié à SQLite utilisant SQLAlchemy ORM.
    """

    def __init__(self, session=None):
        self._custom_session = session

    def _getSession(self):
        """Retourne la session SQLAlchemy courante"""
        if self._custom_session:
            return self._custom_session
        return get_session()

    def findAll(self, edition="FC26", limit=12, offset=0):
        """Trouve les joueurs d'une édition triés par meilleure note"""
        session = self._getSession()
        try:
            query = session.query(Player).filter_by(
                edition=edition
            ).order_by(Player.overall.desc())

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            if not self._custom_session:
                session.close()

    def findById(self, sofifa_id, edition="FC26"):
        """Trouve un joueur par son ID SoFIFA et son édition"""
        session = self._getSession()
        try:
            return session.query(Player).filter_by(
                sofifa_id=sofifa_id,
                edition=edition
            ).first()
        finally:
            if not self._custom_session:
                session.close()

    def findByNameSubword(self, name, edition="FC26", limit=12, offset=0):
        """Recherche les joueurs contenant le nom indiqué"""
        session = self._getSession()
        try:
            pattern = f"%{name}%"
            query = session.query(Player).filter(
                Player.edition == edition,
                Player.name.ilike(pattern)
            ).order_by(Player.overall.desc())

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            if not self._custom_session:
                session.close()

    def _buildCriteriaQuery(self, session, edition="FC26",
                            position=None, min_overall=None,
                            max_age=None, max_budget=None,
                            min_pace=None, min_potential=None,
                            min_shooting=None, min_passing=None,
                            min_dribbling=None, min_defending=None,
                            min_physicality=None, name=None):
        """Construit la requête ORM filtrée selon les critères fournis"""
        query = session.query(Player).filter_by(edition=edition)

        if name:
            query = query.filter(Player.name.ilike(f"%{name}%"))
        if position and position != "ALL":
            query = query.filter(Player.position == position.upper())
        if min_overall is not None:
            query = query.filter(Player.overall >= min_overall)
        if max_age is not None:
            query = query.filter(Player.age <= max_age)
        if max_budget is not None:
            query = query.filter(Player.market_value_eur <= max_budget)
        if min_pace is not None:
            query = query.filter(Player.pace >= min_pace)
        if min_potential is not None:
            query = query.filter(Player.potential >= min_potential)
        if min_shooting is not None:
            query = query.filter(Player.shooting >= min_shooting)
        if min_passing is not None:
            query = query.filter(Player.passing >= min_passing)
        if min_dribbling is not None:
            query = query.filter(Player.dribbling >= min_dribbling)
        if min_defending is not None:
            query = query.filter(Player.defending >= min_defending)
        if min_physicality is not None:
            query = query.filter(Player.physicality >= min_physicality)

        return query

    def findByCriteria(self, edition="FC26",
                       position=None, min_overall=None,
                       max_age=None, max_budget=None,
                       min_pace=None, min_potential=None,
                       min_shooting=None, min_passing=None,
                       min_dribbling=None, min_defending=None,
                       min_physicality=None, name=None,
                       sort="overall_desc", limit=12, offset=0):
        """
        Recherche les joueurs selon les critères sélectionnés,
        avec tri et pagination (limit=12 par défaut).
        """
        session = self._getSession()
        try:
            query = self._buildCriteriaQuery(
                session,
                edition=edition,
                position=position,
                min_overall=min_overall,
                max_age=max_age,
                max_budget=max_budget,
                min_pace=min_pace,
                min_potential=min_potential,
                min_shooting=min_shooting,
                min_passing=min_passing,
                min_dribbling=min_dribbling,
                min_defending=min_defending,
                min_physicality=min_physicality,
                name=name
            )

            # Tri
            if sort == "pace_desc":
                query = query.order_by(Player.pace.desc())
            elif sort == "price_asc":
                query = query.order_by(Player.market_value_eur.asc())
            elif sort == "price_desc":
                query = query.order_by(Player.market_value_eur.desc())
            elif sort == "potential_desc":
                query = query.order_by(Player.potential.desc())
            else:
                query = query.order_by(Player.overall.desc())

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        finally:
            if not self._custom_session:
                session.close()

    def countByCriteria(self, edition="FC26",
                        position=None, min_overall=None,
                        max_age=None, max_budget=None,
                        min_pace=None, min_potential=None,
                        min_shooting=None, min_passing=None,
                        min_dribbling=None, min_defending=None,
                        min_physicality=None, name=None):
        """Compte le nombre de joueurs correspondant aux critères"""
        session = self._getSession()
        try:
            query = self._buildCriteriaQuery(
                session,
                edition=edition,
                position=position,
                min_overall=min_overall,
                max_age=max_age,
                max_budget=max_budget,
                min_pace=min_pace,
                min_potential=min_potential,
                min_shooting=min_shooting,
                min_passing=min_passing,
                min_dribbling=min_dribbling,
                min_defending=min_defending,
                min_physicality=min_physicality,
                name=name
            )
            return query.count()
        finally:
            if not self._custom_session:
                session.close()

    def getNumberOfElements(self, edition="FC26"):
        """Retourne le nombre total de joueurs pour une édition"""
        session = self._getSession()
        try:
            return session.query(Player).filter_by(
                edition=edition
            ).count()
        finally:
            if not self._custom_session:
                session.close()

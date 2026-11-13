from flask import render_template
from . import index_bp
from app.services import player_service, reference_service


@index_bp.route('/')
def index():
    """
    Contrôleur de la page d'accueil :
    Charge les joueurs recommandés du moment et les championnats pour les filtres.
    """
    curated_players = player_service.get_curated_players(limit=4)
    leagues = reference_service.get_leagues()
    return render_template(
        'index.html',
        active_page='home',
        curated_players=curated_players,
        leagues=leagues
    )


@index_bp.route('/manifeste')
def manifeste():
    """Section explicative sur le fonctionnement de la recommandation"""
    curated_players = player_service.get_curated_players(limit=4)
    leagues = reference_service.get_leagues()
    return render_template(
        'index.html',
        active_page='home',
        curated_players=curated_players,
        leagues=leagues
    )

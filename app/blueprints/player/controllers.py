from flask import render_template, request, jsonify, abort
from . import player_bp
from app.services import player_service


@player_bp.route('/<int:player_id>')
def player_detail(player_id=252371):
    """
    Contrôleur de la fiche détaillée d'un joueur :
    Supporte à la fois le rendu complet (HTML) et l'API JSON
    pour la modale Quick View (?format=json).
    """
    player_dict, stats = player_service.get_player_by_id(player_id)

    # Si le joueur n'existe pas en base, fallback sur Bellingham
    if not player_dict:
        player_dict, stats = player_service.get_player_by_id(252371)

    # Réponse JSON pour les requêtes AJAX / modale Quick View
    if request.args.get('format') == 'json' or request.is_json:
        return jsonify(player_dict)

    similar = player_service.get_similar_players(player_dict, limit=4)

    return render_template(
        'player.html',
        player=player_dict,
        stats=stats,
        similar_players=similar,
        active_page='scout'
    )

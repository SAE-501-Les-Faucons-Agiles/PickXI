from flask import render_template, request, jsonify
from . import pitch_bp
from app.services import pitch_service


@pitch_bp.route('', methods=['GET'])
@pitch_bp.route('/', methods=['GET'])
def pitch():
    """
    Contrôleur du terrain tactique (Mon Onze) :
    Affiche le terrain interactif et les recommandations de pépites par poste.
    """
    recommended = pitch_service.get_recommendations_for_slot('ST', limit=4)
    return render_template(
        'pitch.html',
        recommended_players=recommended,
        active_page='pitch'
    )


@pitch_bp.route('/api/recommend/<position_code>')
def api_recommend_position(position_code):
    """
    Retourne en JSON les meilleurs joueurs pour un poste cliqué sur le terrain.
    """
    limit = request.args.get('limit', 4, type=int)
    players = pitch_service.get_recommendations_for_slot(position_code.upper(), limit=limit)
    return jsonify({
        'position': position_code.upper(),
        'players': players
    })


@pitch_bp.route('/api/metrics', methods=['POST'])
def api_squad_metrics():
    """
    Calcule et renvoie en JSON la note générale, la vitesse et le coût cumulé du onze.
    """
    data = request.get_json(silent=True) or {}
    player_ids = data.get('player_ids', [])
    metrics = pitch_service.calculate_squad_metrics(player_ids)
    return jsonify(metrics)


@pitch_bp.route('/api/formation/<formation_name>')
def api_formation_layout(formation_name):
    """
    Retourne les coordonnées géométriques des 11 postes pour une formation donnée.
    """
    coords = pitch_service.get_formation(formation_name)
    return jsonify({
        'formation': formation_name,
        'slots': coords
    })

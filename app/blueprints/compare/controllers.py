from flask import render_template, request, jsonify
from . import compare_bp
from app.services import compare_service, player_service


@compare_bp.route('', methods=['GET'])
@compare_bp.route('/', methods=['GET'])
def compare():
    """
    Contrôleur du Comparateur 1 contre 1 :
    Récupère deux joueurs (via p1 et p2 en paramètre GET),
    génère les écarts statistiques et alimente le radar 6 axes.
    """
    p1_arg = request.args.get('p1', '252371')
    p2_arg = request.args.get('p2', '239053')

    try:
        p1_id = int(p1_arg)
    except ValueError:
        p1_id = 252371

    try:
        p2_id = int(p2_arg)
    except ValueError:
        p2_id = 239053

    # Appel au CompareService
    duel = compare_service.compare_players(p1_id, p2_id)

    return render_template(
        'compare.html',
        p1=duel['p1'],
        p2=duel['p2'],
        comparison=duel,
        active_page='compare'
    )


@compare_bp.route('/api/search')
def api_compare_search():
    """
    Point d'accès API pour la modale de recherche rapide de joueurs
    à substituer dans le comparateur.
    """
    query = request.args.get('q', '').strip()
    position = request.args.get('pos', 'ALL')
    exclude_id = request.args.get('exclude', type=int)

    candidates = compare_service.search_candidates(
        query=query,
        position=position,
        exclude_id=exclude_id,
        limit=20
    )
    return jsonify({'candidates': candidates, 'count': len(candidates)})

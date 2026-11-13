from flask import render_template, request, jsonify
from . import scout_bp
from app.services import player_service, reference_service


@scout_bp.route('', methods=['GET'])
@scout_bp.route('/', methods=['GET'])
def scout():
    """
    Contrôleur du Scout / Détection de joueurs :
    Traite les critères de recherche, les filtres tactiques et la pagination.
    """
    page = request.args.get('page', 1, type=int)

    filters = {
        'q': request.args.get('q', '').strip(),
        'pos': request.args.get('pos', 'ALL'),
        'min_ovr': request.args.get('min_ovr'),
        'min_pace': request.args.get('min_pace'),
        'max_budget': request.args.get('max_budget'),
        'skill_moves': request.args.get('skill_moves'),
        'weak_foot': request.args.get('weak_foot'),
        'max_age': request.args.get('max_age'),
        'preferred_foot': request.args.get('preferred_foot'),
        'league': request.args.get('league', 'ALL'),
        'playstyle': request.args.get('playstyle', 'ALL'),
        'sort': request.args.get('sort', 'overall_desc')
    }

    # Recherche via le PlayerService
    search_result = player_service.search_players(filters, page=page, per_page=12)
    leagues = reference_service.get_leagues()

    return render_template(
        'scout.html',
        players=search_result['players'],
        total_count=search_result['total_count'],
        page=search_result['page'],
        total_pages=search_result['total_pages'],
        current_filters=filters,
        leagues=leagues,
        active_page='scout'
    )


@scout_bp.route('/api/search')
def api_search():
    """
    Point d'accès API JSON pour la recherche dynamique de joueurs (AJAX/Fetch)
    """
    page = request.args.get('page', 1, type=int)
    filters = {
        'q': request.args.get('q', '').strip(),
        'pos': request.args.get('pos', 'ALL'),
        'min_ovr': request.args.get('min_ovr'),
        'min_pace': request.args.get('min_pace'),
        'max_budget': request.args.get('max_budget'),
        'skill_moves': request.args.get('skill_moves'),
        'weak_foot': request.args.get('weak_foot'),
        'max_age': request.args.get('max_age'),
        'preferred_foot': request.args.get('preferred_foot'),
        'league': request.args.get('league', 'ALL'),
        'playstyle': request.args.get('playstyle', 'ALL'),
        'sort': request.args.get('sort', 'overall_desc')
    }

    result = player_service.search_players(filters, page=page, per_page=20)
    return jsonify(result)

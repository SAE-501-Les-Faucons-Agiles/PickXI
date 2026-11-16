from flask import render_template, request, jsonify
from . import scout_bp
from app.services import player_service, reference_service
from flask import current_app
from ollama import ResponseError
from pydantic import ValidationError

from app.services.IARecommendationService import recommander

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
        'sort': request.args.get('sort', 'overall_desc'),
        'min_potential': request.args.get('min_potential'),
        'min_shooting': request.args.get('min_shooting'),
        'min_passing': request.args.get('min_passing'),
        'min_dribbling': request.args.get('min_dribbling'),
        'min_defending': request.args.get('min_defending'),
        'min_physicality': request.args.get('min_physicality')
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
        'sort': request.args.get('sort', 'overall_desc'),
        'min_potential': request.args.get('min_potential'),
        'min_shooting': request.args.get('min_shooting'),
        'min_passing': request.args.get('min_passing'),
        'min_dribbling': request.args.get('min_dribbling'),
        'min_defending': request.args.get('min_defending'),
        'min_physicality': request.args.get('min_physicality')
    }

    result = player_service.search_players(filters, page=page, per_page=20)
    return jsonify(result)


@scout_bp.route('/api/recommend', methods=['POST'])
def api_recommend():
    donnees=request.get_json(silent=True)
    if not isinstance(donnees,dict):
        return jsonify({"error": "Invalid JSON data"}), 400
    description = donnees.get('description')
    if not isinstance(description, str) or not description.strip():
        return jsonify({"error": "Description is required and must be a non-empty string"}), 400
    try:
        resultats = recommander(
            description.strip(),
            avec_explications=False
        )

        recommandations = []

        for resultat in resultats:
            joueur = resultat["joueur"]

            recommandations.append({
                "joueur": {
                    "sofifa_id": joueur.sofifa_id,
                    "name": joueur.name,
                    "club": joueur.club,
                    "position": joueur.position,
                    "age": joueur.age,
                    "overall": joueur.overall,
                    "market_value_eur": joueur.market_value_eur
                },
                "explication": resultat["explication"]
            })

        return jsonify({"recommandations": recommandations})

    except (ConnectionError, ResponseError):
        current_app.logger.exception("Erreur Ollama")
        return jsonify({
            "erreur": "Ollama est indisponible ou llama3.2 est inaccessible."
        }), 503

    except ValidationError:
        current_app.logger.exception("Critères IA invalides")
        return jsonify({
            "erreur": "La demande n'a pas pu être interprétée. Reformule-la."
        }), 422

    except Exception:
        current_app.logger.exception("Erreur de recommandation")
        return jsonify({
            "erreur": "La recherche a échoué."
        }), 500
from flask import Blueprint, jsonify, request
from app.models.player_model import PlayerFilter
from app.services.player_repository import player_repository
from app.services.recommendation_service import recommendation_service
from app.services.metrics_service import metrics_service

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/players", methods=["GET"])
def get_players():
    """Retourne la liste des joueurs disponibles."""
    players = player_repository.get_all()
    return jsonify({
        "status": "success",
        "count": len(players),
        "data": [p.to_dict() for p in players]
    }), 200

@api_bp.route("/recommend", methods=["POST"])
def recommend_players():
    """
    Endpoint principal découplé :
    Reçoit les critères de recherche et renvoie les résultats des 2 approches
    ainsi que les métriques d'optimisation (temps, complexité, impact batterie).
    """
    payload = request.get_json(silent=True) or {}

    player_filter = PlayerFilter(
        position=payload.get("position", "ALL"),
        max_price=int(payload.get("max_price", 3000000)),
        min_weak_foot=int(payload.get("min_weak_foot", 3)),
        target_club=payload.get("target_club", ""),
        target_league=payload.get("target_league", ""),
        target_nationality=payload.get("target_nationality", ""),
        weight_pace=float(payload.get("weight_pace", 1.0)),
        weight_shooting=float(payload.get("weight_shooting", 1.0)),
        weight_passing=float(payload.get("weight_passing", 1.0)),
        weight_dribbling=float(payload.get("weight_dribbling", 1.0)),
        weight_defending=float(payload.get("weight_defending", 1.0)),
        weight_physic=float(payload.get("weight_physic", 1.0))
    )

    limit = int(payload.get("limit", 6))
    comparison = recommendation_service.run_comparison(player_filter, limit=limit)

    return jsonify({
        "status": "success",
        "approaches": {
            "vector_cosine": comparison["vector_cosine"].to_dict(),
            "chemistry_graph": comparison["chemistry_graph"].to_dict()
        }
    }), 200

@api_bp.route("/metrics/summary", methods=["GET"])
def get_metrics_summary():
    """Statistiques d'exécution globales des algorithmes."""
    return jsonify({
        "status": "success",
        "history": metrics_service.history
    }), 200

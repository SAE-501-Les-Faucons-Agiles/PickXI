from flask import Blueprint, render_template, request
from app.models.player_model import PlayerFilter
from app.services.player_repository import player_repository
from app.services.recommendation_service import recommendation_service

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET", "POST"])
def index():
    # Récupération des filtres depuis la requête GET ou POST
    data = request.form if request.method == "POST" else request.args

    position = data.get("position", "BU")
    max_price = int(data.get("max_price", 3000000))
    min_weak_foot = int(data.get("min_weak_foot", 3))
    target_club = data.get("target_club", "Real Madrid")
    target_league = data.get("target_league", "LaLiga")
    target_nationality = data.get("target_nationality", "France")
    active_tab = data.get("tab", "compare")

    # Poids des statistiques prioritaires
    w_pac = float(data.get("w_pac", 1.0))
    w_sho = float(data.get("w_sho", 0.9))
    w_pas = float(data.get("w_pas", 0.7))
    w_dri = float(data.get("w_dri", 0.8))
    w_def = float(data.get("w_def", 0.3))
    w_phy = float(data.get("w_phy", 0.6))

    player_filter = PlayerFilter(
        position=position,
        max_price=max_price,
        min_weak_foot=min_weak_foot,
        target_club=target_club,
        target_league=target_league,
        target_nationality=target_nationality,
        weight_pace=w_pac,
        weight_shooting=w_sho,
        weight_passing=w_pas,
        weight_dribbling=w_dri,
        weight_defending=w_def,
        weight_physic=w_phy
    )

    comparison = recommendation_service.run_comparison(player_filter, limit=6)

    # Données pour les listes déroulantes de filtres
    all_clubs = player_repository.get_unique_clubs()
    all_leagues = player_repository.get_unique_leagues()
    all_nations = player_repository.get_unique_nationalities()
    positions = ["ALL", "BU", "AG", "AD", "MOC", "MC", "MDC", "DC", "DG", "DD", "G"]

    return render_template(
        "index.html",
        filter=player_filter,
        vector_res=comparison["vector_cosine"],
        chem_res=comparison["chemistry_graph"],
        total_candidates=comparison["total_candidates"],
        all_clubs=all_clubs,
        all_leagues=all_leagues,
        all_nations=all_nations,
        positions=positions,
        active_tab=active_tab
    )

@home_bp.route("/players")
def players_list():
    players = player_repository.get_all()
    return render_template("players.html", players=players)

@home_bp.route("/about")
def about():
    return render_template("about.html")

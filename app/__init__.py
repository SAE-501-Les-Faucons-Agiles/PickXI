import os
from flask import Flask
from app.config import config_by_name
from app.controllers import home_bp, api_bp
from app.database import init_app, init_db


def create_app(config_name: str = "default") -> Flask:
    """
    Application Factory Flask respectant les bonnes pratiques.
    Configure SQLite et enregistre les contrôleurs Blueprints MVC.
    """
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_by_name[config_name])

    # Mode dev : cookie de session non sécurisé (HTTP)
    app.config["SESSION_COOKIE_SECURE"] = False

    # Initialisation de la base SQLite et des hooks d'application
    init_app(app)

    # Enregistrement des Blueprints (Contrôleurs MVC)
    app.register_blueprint(home_bp)
    app.register_blueprint(api_bp)

    return app


# Instance par défaut pour imports directs (ex: main.py)
app = create_app(os.environ.get("FLASK_ENV", "default"))

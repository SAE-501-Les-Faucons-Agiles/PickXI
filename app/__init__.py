import os
from flask import Flask


def create_app():
	app = Flask(
		__name__,
		static_folder='static',
		static_url_path='/static',
		template_folder='templates'
	)

	app.config["SESSION_COOKIE_SECURE"] = False  # dev mode

	# Enregistrement centralisé des Blueprints / Contrôleurs modulaires
	from app.blueprints import (
		index_bp,
		scout_bp,
		compare_bp,
		pitch_bp,
		player_bp
	)

	app.register_blueprint(index_bp)
	app.register_blueprint(scout_bp)
	app.register_blueprint(compare_bp)
	app.register_blueprint(pitch_bp)
	app.register_blueprint(player_bp)

	return app


# Instance exportée requise par main.py
app = create_app()


import os
from flask import Flask


def create_app():
	app = Flask(__name__, static_url_path='/static')


	app.config["SESSION_COOKIE_SECURE"] = False  # dev mode
	

	#from app.blueprints import ()

	#app.register_blueprint(?)
	return app

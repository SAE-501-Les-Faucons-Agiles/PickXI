import os
from flask import Flask, render_template


def create_app():
	app = Flask(
		__name__,
		static_folder='static',
		static_url_path='/static',
		template_folder='templates'
	)

	app.config["SESSION_COOKIE_SECURE"] = False  # dev mode

	# Routes de rendu des templates front-end
	@app.route('/')
	def index():
		return render_template('index.html', active_page='home')

	@app.route('/scout')
	def scout():
		return render_template('scout.html', active_page='scout')

	@app.route('/pitch')
	def pitch():
		return render_template('pitch.html', active_page='pitch')

	@app.route('/compare')
	def compare():
		return render_template('compare.html', active_page='compare')

	@app.route('/player/<int:player_id>')
	def player(player_id=252371):
		return render_template('player.html', active_page='scout')

	#from app.blueprints import ()
	#app.register_blueprint(?)

	return app


# Instance exportée requise par main.py
app = create_app()


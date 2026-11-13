from flask import Blueprint

pitch_bp = Blueprint(
    'pitch',
    __name__,
    url_prefix='/pitch',
    template_folder='templates'
)

from . import controllers

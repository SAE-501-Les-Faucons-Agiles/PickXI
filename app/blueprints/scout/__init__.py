from flask import Blueprint

scout_bp = Blueprint(
    'scout',
    __name__,
    url_prefix='/scout',
    template_folder='templates'
)

from . import controllers

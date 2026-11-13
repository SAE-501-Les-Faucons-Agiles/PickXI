from flask import Blueprint

compare_bp = Blueprint(
    'compare',
    __name__,
    url_prefix='/compare',
    template_folder='templates'
)

from . import controllers

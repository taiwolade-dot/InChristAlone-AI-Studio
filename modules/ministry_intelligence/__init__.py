from flask import Blueprint

ministry_intelligence_bp = Blueprint(
    "ministry_intelligence",
    __name__,
    template_folder="templates"
)

from . import routes

from flask import Blueprint, render_template
from flask_login import login_required
from .data import TUTORIALS

help_center_bp = Blueprint(
    'help_center',
    __name__,
    url_prefix='/help',
    template_folder='../../templates/help_center'
)


@help_center_bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('help_center/index.html', tutorials=TUTORIALS)

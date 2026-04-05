from flask import Blueprint

bp_p_menubar = Blueprint('bp_p_menubar', __name__)


@bp_p_menubar.route('/menubar')
def index():
    from flask import render_template

    return render_template('__menu_top.html')

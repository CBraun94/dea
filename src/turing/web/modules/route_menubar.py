from flask import Blueprint

bp_p_menubar = Blueprint('bp_p_menubar', __name__)

ROUTE_MENUBAR_ROOT = '/menubar'


@bp_p_menubar.route(ROUTE_MENUBAR_ROOT)
def index():
    from flask import render_template

    return render_template('__menu_top.html')

from flask import Blueprint

bp_p_about = Blueprint('bp_p_about', __name__)

ROUTE_ABOUT_ROOT = '/about'


@bp_p_about.route(ROUTE_ABOUT_ROOT)
def prepare_template_about():
    from flask import render_template

    html = render_template(template_name_or_list='about.html')

    return html

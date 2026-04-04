from flask import Blueprint

bp_p_about = Blueprint('bp_p_about', __name__)


@bp_p_about.route('/about')
def prepare_template_about():
    from flask import render_template

    html = render_template(template_name_or_list='about.html')

    return html

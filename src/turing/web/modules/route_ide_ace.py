from flask import Blueprint

bp_p_ide_ace = Blueprint('bp_p_ide_ace', __name__)

ROUTE_IDE_ACE_ROOT = '/ide'
ROUTE_IDE_ACE_RUN = '/ide/run'

@bp_p_ide_ace.route(ROUTE_IDE_ACE_ROOT)
def index():
    from flask import render_template

    return render_template('ide_ace.html')


@bp_p_ide_ace.route(ROUTE_IDE_ACE_RUN, methods=['POST'])
def run_code():
    from flask import request, jsonify
    from io import StringIO
    import sys

    code = request.json['code']
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        exec(code)
        sys.stdout = old_stdout
        return jsonify({'output': redirected_output.getvalue()})
    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({'output': str(e)})

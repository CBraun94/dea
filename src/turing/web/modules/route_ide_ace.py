from flask import Blueprint

bp_p_ide_ace = Blueprint('bp_p_ide_ace', __name__)


@bp_p_ide_ace.route('/ide')
def index():
    from flask import render_template

    return render_template('ide_ace.html')


@bp_p_ide_ace.route('/ide/run', methods=['POST'])
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

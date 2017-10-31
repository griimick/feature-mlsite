from flask import Blueprint, render_template

team_mod = Blueprint('team', __name__, template_folder='templates', static_folder='static')


@team_mod.route('/team')
def team():
    return render_template('team.html')
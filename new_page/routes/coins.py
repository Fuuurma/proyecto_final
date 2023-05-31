from flask import Blueprint, render_template

coins = Blueprint('coins', __name__)

@coins.route('/coin')
def do_something():
    return render_template('coins_general.html')


from flask import Blueprint, render_template

chains = Blueprint('coins', __name__)

@chains.route('/chains')
def do_something():
    return render_template('chains.html')
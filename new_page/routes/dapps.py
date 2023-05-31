from flask import Blueprint, render_template

dapps = Blueprint('coins', __name__)

@dapps.route('/dapps')
def do_something():
    return render_template('dapps.html')
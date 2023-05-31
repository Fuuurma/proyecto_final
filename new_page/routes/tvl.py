from flask import Blueprint, render_template

tvl = Blueprint('coins', __name__)

@tvl.route('/tvl')
def do_something():
    return render_template('tvl.html')
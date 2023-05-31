from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from routes.coins import coins
from routes.tvl import tvl
from routes.chains import chains
from routes.dapps import dapps

user = 'root'
password = 240699
host = '127.0.0.1'
port = 3306
database = 'data_crypto'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class tvl_historic(db.Model):
    
    index = db.Column(db.Integer, primary_key=True)
    tvl_historic = db.Column(db.Decimal)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<tvl_historic %r>' % self.date


@app.route('/')
def home():
  
    return render_template('home.html')


# app.register_blueprint(coins)
# app.register_blueprint(tvl)
# app.register_blueprint(chains)
# app.register_blueprint(dapps)











 
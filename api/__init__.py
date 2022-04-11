from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

db_name = "postgresql://lucca10:goku6060@localhost/redditdb"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_name

db= SQLAlchemy(app)

from api import views

# @app.route('/hello')
# def hello_world():
#    return "hello world"

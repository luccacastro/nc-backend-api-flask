from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

db_name = "postgresql://wcrtwhjnndfkkf:a4f5ac23e1ca034d8e70ca13d3d1e893274db26472d0ded806cf19caf529b6c7@ec2-44-194-4-127.compute-1.amazonaws.com:5432/d2fkeg4fjpaki5"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_name

db= SQLAlchemy(app)

from api import views

# @app.route('/hello')
# def hello_world():
#    return "hello world"

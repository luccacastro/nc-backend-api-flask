from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

db_name = "postgresql://yquaerpsqackgn:ff62107d5a6ac51618654f2ea7623ea373a465a6b8728a6f30ffaec130090477@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d566hhhscc32ai"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_name

db= SQLAlchemy(app)

from api import views

# @app.route('/hello')
# def hello_world():
#    return "hello world"

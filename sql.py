from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lucca10:goku6060@localhost/testdb"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(100))
    pets = db.relationship('Pet', backref='owner')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

anthony = Owner(name='johnlefucker', address='evergreen road 19')    
owner = Owner.query.filter_by(name='dssd').one()
print(owner)
# pet = Pet(name='spronkus',age=2,owner=owner)
# print(pet.owner.name)
# db.session.add(pet)
# db.session.commit()
# print()
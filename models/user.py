from flask_login import UserMixin
from database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    meal = db.relationship('Meal', backref='author', lazy=True)
    

class Meals(db.Model):
    id = db.Columm(db.integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.string(300), nullable=True)
    mealtime = db.Column(db.string(20), nullable=True)
    indiet = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.integer, db.ForeignKey('user.id'), nullable=False)


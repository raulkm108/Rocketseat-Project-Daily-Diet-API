from flask_login import UserMixin
from database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    meal = db.relationship('Meal', back_populates='user')
    

class Meal(db.Model, UserMixin):
    id = db.Columm(db.integer, primary_key=True)
    user_id = db.ForeignKey('User', back_populates='meals')
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.string(300), nullable=True)
    mealtime = db.column(db.string(20), nullable=True)
    indiet = db.column(db.Bool, nullable=False)


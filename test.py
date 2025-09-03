from database import db
from models.user import User, Meal
from app import app

with app.app_context():

    id_user = 1

    user = User.query.get(id_user)
    for meal in user.meals:
        print(meal)
    
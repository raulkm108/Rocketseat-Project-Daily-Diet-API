from database import db
from models.user import User, Meal
from app import app

with app.app_context():

    id_user = 2

    user = User.query.get(id_user)
    
    print(f"{user.meals}")
    
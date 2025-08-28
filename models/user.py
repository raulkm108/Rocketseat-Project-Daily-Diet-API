from flask_login import UserMixin
from database import db

class User(db.Model, UserMixin):
    pass

from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)
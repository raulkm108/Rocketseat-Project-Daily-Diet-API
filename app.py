from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
         user = User.query.filter_by(username=username). first()
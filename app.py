from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

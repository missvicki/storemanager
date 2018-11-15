from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import app_config
app = Flask(__name__, instance_relative_config=True)

from api import views

# Setup flask-jwt-extended
app.config['JWT_SECRET_KEY'] = 'secret'
app.config.from_object(app_config["development"])
jwt = JWTManager(app)
CORS(app)

# index route
@app.route('/')
def hello():
    """my home"""
    return render_template("index.html")

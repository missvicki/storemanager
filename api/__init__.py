from flask import Flask, render_template
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from api import views

# Setup flask-jwt-extended
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

# index route
@app.route('/')
def hello():
    """my home"""
    return render_template("index.html")
    
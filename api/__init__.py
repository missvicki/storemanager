from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__, instance_relative_config=True)

from api import views

# Setup flask-jwt-extended
app.config['JWT_SECRET_KEY'] = 'secret'

# Enable blacklisting and specify what kind of tokens to check
# against the blacklist
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

#cross origin
CORS(app)
    
# index route
@app.route('/')
def hello():
    """my home"""
    return render_template("index.html")
    
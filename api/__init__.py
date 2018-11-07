from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# Setup flask-jwt-extended
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)


from api import views
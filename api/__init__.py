from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(config_name):
    app = Flask(__name__)
    # Setup flask-jwt-extended
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config.from_object(config_name)
    jwt = JWTManager(app)
    return app

app = create_app('config.TestingConfig')


from api import views
from flask import json
from flask_jwt_extended import create_access_token
import pytest
from api.views import app
from models.usersModel import Login

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_login_(client):
    with app.app_context():
        username = 'vickib'
        user_pass = 'vibel'
        role = 'admin'
        auth = Login(username, user_pass, role)
        res = client.post('/api/v1/auth/login', data = json.dumps(dict(
            use_rname = auth.user_name,
            password = auth.password,
            role = auth.role
        )),content_type='application/json')
        assert res.status_code == 200
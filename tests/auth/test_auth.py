import pytest
from flask import jsonify
from werkzeug.security import check_password_hash
from app import create_app, mongo

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }

@pytest.fixture
def login_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword"
    }

def test_signup_valid(client, user_data):
    """Test the signup route with valid data."""
    response = client.post('/auth/signup', json=user_data)
    assert response.status_code == 201
    assert b"User registered successfully" in response.data

    # Verify if the user is in the database
    user = mongo.db.users.find_one({"email": user_data["email"]})
    assert user is not None
    assert user["email"] == user_data["email"]
import pytest
from app import create_app, mongo
from werkzeug.security import generate_password_hash
import logging
from app.models import database_models
from datetime import datetime, timezone


logging.basicConfig(level=logging.INFO)


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
        "username": "user",
        "email": "user@example.com",
        "password": "userpassword",
        # "role": "admin",
    }


@pytest.fixture
def login_data():
    return {"email": "user@example.com", "password": "userpassword"}


@pytest.fixture
def setup_user_in_db(user_data):

    hashed_password = generate_password_hash(user_data["password"])

    existing_user = mongo.db.users.find_one({"email": user_data["email"]})

    role = user_data.get("role", "user").strip().lower()
    if not role in ["admin", "user"]:
        logging.info(f"Invalid role provided: {role}")

    if not existing_user:
        user_model = database_models.get_user_model()

        user_model["username"] = user_data["username"]
        user_model["email"] = user_data["email"]
        user_model["password"] = hashed_password
        user_model["role"] = role
        user_model["deleted"] = False
        user_model["created_at"] = user_model["updated_at"] = datetime.now(timezone.utc)

        mongo.db.users.insert_one(user_model)

        logging.info(f"Inserted user: {user_data['email']}")
    else:
        logging.info(f"User {user_data['email']} already exists.")

    yield

    mongo.db.users.delete_one({"email": user_data["email"]})
    logging.info(f"Test user deleted {user_data["email"]}")

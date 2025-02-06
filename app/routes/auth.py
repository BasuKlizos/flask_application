import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import database_models
from .. import mongo


auth_blueprint = Blueprint("auth", __name__)

EMAIL_REGEX = r"^[a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"


# Root endpoint
@auth_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"msg": "Welcome to Flask-based API's Application"}), 200


# Signup endpoint
@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Invalid input"}), 400

    username = data["username"].strip()
    email = data["email"].strip()
    password = data["password"].strip()

    # Username validation
    if len(username) < 3 or len(username) > 20:
        return jsonify({"error": "Username must be between 3 and 20 characters"}), 400

    if not username.isalnum():
        return jsonify({"error": "Username must be alphanumeric"}), 400

    # Email validation
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    # Username and email already exists

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    # role = data.get("role", "user").strip().lower()

    # if role not in ["user", "admin"]:
    #     return jsonify({"error": "Invalid role specified"}), 400

    if "role" in data:
        return jsonify({"error": "You cannot specify the role during signup. The role is automatically assigned."}), 400

    existing_role = mongo.db.users.find_one({"role": "admin"})

    if not existing_role:
        role = "admin"
    else:
        role = "user"

    hashed_password = generate_password_hash(password)

    user_model = database_models.get_user_model()

    user_model["username"] = username
    user_model["email"] = email
    user_model["password"] = hashed_password
    user_model["role"] = role

    mongo.db.users.insert_one(user_model)

    return jsonify({"message": "User registered successfully"}), 201


# Login endpoint
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"].strip()
    password = data["password"].strip()

    user = mongo.db.users.find_one({"email": email})

    if user and check_password_hash(user["password"], password):
        access_token = create_access_token(identity=str(user["_id"]))
        refresh_token = create_refresh_token(identity=str(user["_id"]))
        return (
            jsonify({"access_token": access_token, "refresh_token": refresh_token}),
            200,
        )

    return jsonify({"error": "Invalid credentials"}), 401

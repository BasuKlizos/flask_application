from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import database_models
from .. import mongo


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"msg": "Hello world"}), 200


@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Invalid input"}), 400

    user_model = database_models.get_user_model()

    hashed_password = generate_password_hash(data["password"])

    role = data.get("role", "user")

    if role not in ["user", "admin"]:
        return jsonify({"error": "Invalid role specified"}), 400

    user_model["username"] = data["username"]
    user_model["email"] = data["email"]
    user_model["password"] = hashed_password
    user_model["role"] = role

    mongo.db.users.insert_one(user_model)

    return jsonify({"message": "User registered successfully"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    if (
        not data
        or not all(k in data for k in ("email", "password"))
        or not data["email"].strip()
        or not data["password"].strip()
    ):
        return jsonify({"error": "Email and password are required"}), 400

    user = mongo.db.users.find_one({"email": data["email"]})

    if user and check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=str(user["_id"]))
        # refresh_token = create_refresh_token(identity=str(user["_id"]))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

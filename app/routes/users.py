from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from .. import mongo
from datetime import datetime, timezone
from app.models import database_models
from werkzeug.security import generate_password_hash
from app.utils.role_utils import role_required

users_blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_blueprint.route("/", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_users():
    users = mongo.db.users.find({"deleted": False})
    print(users)
    response_data = []

    for user in users:
        response_data.append({
            "id": str(user["_id"]),
            "username":user["username"],
            "email": user["email"],
            "role": user["role"],
            "deleted": user.get("deleted", False),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        })
    
    return jsonify(response_data),200


@users_blueprint.route("/<user_id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_user_by_id(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"deleted": False})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return (
        jsonify(
            {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "created_at": user.get("created_at", None),
                "updated_at": user.get("updated_at", None),
                "deleted": user.get("deleted", False),
            }
        ),
        200,
    )


@users_blueprint.route("/<user_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_user_by_id(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"deleted": False})
    if not user:
        return jsonify({"error": "User not found"}), 404

    allowed_fields = ["username", "email", "password"]
    updated_data = {}

    for field in allowed_fields:
        if field in request.json:
            updated_data[field] = request.json[field]

    if "password" in request.json:
        updated_data["password"] = generate_password_hash(request.json["password"])

    updated_data["updated_at"] = datetime.now(timezone.utc)

    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    return jsonify({"message": "User updated"}), 200


@users_blueprint.route("/<user_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_user(user_id):
    current_user = get_jwt_identity()

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    trash_model = database_models.get_trash_model()
    trash_model["original_user_id"] = ObjectId(user_id)
    trash_model["deleted_at"] = datetime.now(timezone.utc)
    trash_model["deleted_by"] = current_user
    trash_model["reason"] = request.json.get("reason", "No reason provided")

    mongo.db.trash.insert_one(trash_model)

    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})
    return jsonify({"message": "User soft-deleted"}), 200


@users_blueprint.route("/batch-delete", methods=["POST"])
@jwt_required()
@role_required("admin")
def batch_delete_users():
    data = request.json
    user_ids = data.get("user_ids", [])

    if not user_ids:
        return jsonify({"error": "No user IDs provided"}), 400

    current_user = get_jwt_identity()

    users = mongo.db.users.find(
        {"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}, "deleted": False}
    )
    print(users)

    for user in users:
        trash_model = database_models.get_trash_model()

        trash_model["original_user_id"] = user["_id"]
        trash_model["deleted_at"] = datetime.now(timezone.utc)
        trash_model["deleted_by"] = current_user
        trash_model["reason"] = data.get("reason", "No reason provided")

        mongo.db.trash.insert_one(trash_model)

        mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"deleted": True}})

    return jsonify({"message": f"soft-deleted {len(user_ids)} users"}), 200


@users_blueprint.route("/trash", methods=["GET"])
@jwt_required()
@role_required("admin")
def view_trash():
    trashed_users = mongo.db.trash.find()
    response_trashed_users = []

    for trashed_user in trashed_users:
        response_trashed_users.append({
            "id": str(trashed_user["original_user_id"]),
            "deleted_at":trashed_user["deleted_at"],
            "deleted_by": trashed_user["deleted_by"],
            "reason": trashed_user["reason"],
        })
    
    return jsonify(response_trashed_users),200


@users_blueprint.route("/restore/<user_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def restore_user(user_id):
    user = mongo.db.trash.find_one({"original_user_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found in trash"}), 404

    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": False}})
    mongo.db.trash.delete_one({"original_user_id": ObjectId(user_id)})

    return jsonify({"message": "User restored"}), 200


@users_blueprint.route("/trash/<user_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def permanent_delete_user(user_id):
    user = mongo.db.trash.find_one({"original_user_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found in trash"}), 404

    mongo.db.trash.delete_one({"original_user_id": ObjectId(user_id)})
    return jsonify({"message": "User permanently deleted"}), 200


# @users_blueprint.route("/promote/<user_id>", methods=["POST"])
# @jwt_required()
# @role_required("admin")  # Only an admin can promote a user
# def promote_to_admin(user_id):
#     user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     if user["role"] == "admin":
#         return jsonify({"message": "User is already an admin"}), 200

#     mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": "admin"}})
#     return jsonify({"message": f"User {user['username']} promoted to admin"}), 200


# @users_blueprint.route("/admin/demote/<user_id>", methods=["POST"])
# @jwt_required()
# @role_required("admin")
# def demote_user(user_id):
#     user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     if user["role"] == "user":
#         return jsonify({"message": "User is already a regular user"}), 200

#     mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": "user"}})
#     return jsonify({"message": f"User {user['username']} demoted to user"}), 200
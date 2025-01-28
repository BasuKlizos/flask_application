from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app import mongo
from bson.objectid import ObjectId

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()  # Get the logged-in user ID from the token
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user["role"] != role:  # Check if the user has the correct role
                return jsonify({"error": "Access forbidden"}), 403  # Forbidden access for non-admins
            return fn(*args, **kwargs)
        return wrapper
    return decorator  


@users_blueprint.route("/promote/<user_id>", methods=["POST"])
@jwt_required()
@role_required("admin")  # Only an admin can promote a user
def promote_to_admin(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user["role"] == "admin":
        return jsonify({"message": "User is already an admin"}), 200

    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": "admin"}})
    return jsonify({"message": f"User {user['username']} promoted to admin"}), 200
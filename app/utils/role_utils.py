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
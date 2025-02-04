import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import uuid


media_blueprint = Blueprint("media", __name__, url_prefix="/media")


def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# if not os.path.exists(UPLOAD_FOLDER):
#     try:
#         os.makedirs(UPLOAD_FOLDER)
#         print(f"Folder created: {UPLOAD_FOLDER}")
#     except Exception as e:
#         print(f"Error creating folder: {e}")


@media_blueprint.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        unique_id = str(uuid.uuid4()).replace("-", "")[:8]
        split_uuid = [unique_id[i : i + 4] for i in range(0, len(unique_id), 4)]
        formatted_uuid = "_".join(split_uuid)

        unique_filename = formatted_uuid + "_" + filename

        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Debugging prints
        print(f"Saving file to: {file_path}")

        try:
            # Save the file to the specified path
            file.save(file_path)
            print(f"File saved successfully at: {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({"error": f"Failed to save file. Error: {e}"}), 500

        file_url = f"/static/media/{unique_filename}"

        return (
            jsonify(
                {"message": "File uploaded successfully", "file_url": f"{file_url}"}
            ),
            200,
        )

    return (
        jsonify({"error": "Invalid file type. Allowed types are png, jpg, jpeg"}),
        400,
    )

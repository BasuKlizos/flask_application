from flask_jwt_extended import create_access_token
from app import mongo
from bson import ObjectId
from datetime import timezone, datetime


def test_get_users(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.get("/users/", headers=headers)

    assert resp.status_code == 200
    assert isinstance(resp.json, list)


def test_get_user_by_id(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.get(f"/users/{user_id}", headers=headers)

    assert resp.status_code == 200
    assert resp.json["id"] == user_id
    assert resp.json["username"] == setup_user_in_db["username"]


# def test_get_user_by_id_valid(setup_user_in_db,client,login_data):
#     response = client.post("/login", json=login_data)

#     assert response.status_code == 200
#     access_token = response.get_json()["access_token"]

#     user_id = str(setup_user_in_db["_id"])
#     # mongo.db.users.update_one({"_id":ObjectId(user_id)}, {"$set": {"deleted": True}})
#     mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})

#     headers = {"Authorization": f"Bearer {access_token}"}

#     resp = client.get(f"/users/{user_id}", headers=headers)

#     assert resp.status_code == 404
#     assert resp.json["error"] == "User not found"


def test_update_user_by_id(client, setup_user_in_db, login_data):

    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = {"username": "updated_username"}
    resp = client.put(f"/users/{user_id}", json=update_data, headers=headers)

    assert resp.status_code == 200
    assert resp.json["message"] == "User updated"


def test_delete_user(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.delete(
        f"/users/{user_id}", json={"reason": "Test delete"}, headers=headers
    )

    assert resp.status_code == 200
    assert resp.json["message"] == "User soft-deleted"


def test_batch_delete_users(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(
        "/users/batch-delete", json={"user_ids": [user_id]}, headers=headers
    )

    assert response.status_code == 200
    assert response.json["message"] == "soft-deleted 1 users"


def test_view_trash(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.get("/users/trash", headers=headers)

    assert resp.status_code == 200
    assert isinstance(resp.json, list)


def test_restore_user(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    # Soft delete user before restoring
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})

    # Add the user to trash for restoration
    mongo.db.trash.insert_one(
        {
            "original_user_id": ObjectId(user_id),
            "deleted_at": datetime.now(timezone.utc),
            "deleted_by": "user_id",
            "reason": "Test",
        }
    )

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.post(f"/users/restore/{user_id}", headers=headers)

    assert resp.status_code == 200
    assert resp.json["message"] == "User restored"


def test_permanent_delete_user(client, setup_user_in_db, login_data):
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    access_token = response.get_json()["access_token"]

    user_id = str(setup_user_in_db["_id"])

    # Soft delete user before permanent deletion
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True}})

    # Add the user to the trash collection
    mongo.db.trash.insert_one(
        {
            "original_user_id": ObjectId(user_id),
            "deleted_aot": datetime.now(timezone.utc),
            "deleted_by": "user_id",
            "reason": "Test for permanent",
        }
    )

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.delete(f"/users/trash/{user_id}", headers=headers)

    assert resp.status_code == 200
    assert resp.json["message"] == "User permanently deleted"

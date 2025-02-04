import logging
from app import mongo


logging.basicConfig(level=logging.INFO)

# For signup endpoint
def test_signup_valid(client, user_data):
    response = client.post("/signup", json=user_data)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"

    user = mongo.db.users.find_one({"email": user_data["email"]})
    assert user is not None
    assert user["username"] == user_data["username"]

    mongo.db.users.delete_one({"email": user_data["email"]})
    logging.info(f"Test user deleted: {user_data["email"]}")

def test_signup_missing_fields(client):
    user_date = {
        "username":"newuser",
        "password":"1234"
    }
    response = client.post("/signup", json = user_date)
    
    assert response.status_code == 400
    assert response.json["error"] == "Invalid input"

def test_signup_username_characters(client):
    user_data = {
        "username": "ba",
        "email": "newuser@gmail.com",
        "password": "1234"
    }

    response = client.post("/signup", json = user_data)

    assert response.status_code == 400
    assert response.json["error"] == "Username must be between 3 and 20 characters"

def test_signup_username_invalid(client):
    user_data = {
        "username": "newuser-1234",
        "email": "newuser1234@gmail.com",
        "password": "12345"
    }

    response =  client.post("/signup", json = user_data)

    assert response.status_code == 400
    assert response.json["error"] == "Username must be alphanumeric"

def test_signup_email_invalid(client):
    user_data = {
        "username" : "newuser",
        "email" : "newuser@gmail..com",
        "password": "1234"
    }

    response = client.post("/signup", json = user_data)

    assert response.status_code == 400
    assert response.json["error"] == "Invalid email format"


def test_signup_username_already_exists(client, user_data, setup_user_in_db):
    response = client.post("/signup", json=user_data)

    assert response.status_code == 400
    assert response.json["error"] == "Username already exists"

def test_signup_useremail_already_exists(client, user_data, setup_user_in_db):
    new_user_data = {
        "username" : "newuser",
        "email" : user_data["email"],
        "password" : "1234"
    }

    response = client.post("/signup", json = new_user_data)

    assert response.status_code == 400
    assert response.json["error"]  == "Email already exists"

def test_signup_role_invalid(client):
    user_data = {
        "username":"newuser",
        "email" : "newuser@gmail.com",
        "password": "1234",
        "role": "guest"
    }

    response = client.post("/signup", json = user_data)

    assert response.status_code == 400
    assert response.json["error"] == "Invalid role specified"



# def test_username


# def test_login_valid(client, setup_user_in_db, user_data):
#     response = client.post("/login", json={
#         "email": user_data["email"], 
#         "password": user_data["password"]
#         })
#     assert response.status_code == 200
#     assert "access_token" in response.json


# def test_login_invalid_email(client, user_data):
#     """
#     Test case for login with an invalid email.
#     """
#     response = client.post("/login", json={
#         "email": "invalid@example.com",  # Non-existent email
#         "password": user_data["password"]
#     })
    
#     # Assertions
#     assert response.status_code == 401  # Unauthorized
#     assert "error" in response.json
#     assert response.json["error"] == "Invalid credentials"

# def test_login_invalid_password(client, setup_user_in_db, user_data):
#     response = client.post("/login", json={"email": user_data["email"], "password": "wrongpassword"})
#     assert response.status_code == 401
#     assert response.json["error"] == "Invalid credentials"
    
    
# def test_login_missing_fields(client):
#     response = client.post("/login", json={})
#     assert response.status_code == 400
#     assert response.json["error"] == "Email and password are required"
    
# def test_login_empty_fields(client):
#     response = client.post("/login", json={"email": "", "password": ""})
#     assert response.status_code == 400
#     assert response.json["error"] == "Email and password are required"
    
# def test_login_invalid_credentials(client, user_data):
#     response = client.post("/login", json={
#         "email": user_data["email"],
#         "password": "wrongpassword"
#     })
#     assert response.status_code == 401
#     assert response.json["error"] == "Invalid credentials"
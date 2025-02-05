# User Management API

**Flask-based API** for managing users, including resgistration, login, and CRUD operations.

## Features

- **User Registration**
- **User login (JWT Authentication)**
- **CRUD operations** (Create, Read, Update, Delete)
- **User promotion/demotion** (admin role)
- **User can upload image**
- **Soft-delete and restore users**
- **Permanent delete from trash**

## Getting started

Follow these steps to set up the project locally:

## Clone the repository

- **bash:** git clone https://github.com/BasuKlizos/flask_application.git
- cd flask_application

## Setup a virtual enviroment

- **bash**
  **Run:** python -m venv .venv
  **For macOS/Linux:** source .venv/bin/activate
  **For Windows:** .venv\Scripts\activate

## Install dependencies

- **bash**
  - python -m pip install --upgrade pip
  - pip install -r requirements.txt

## Run the application:

- **python main.py**

## Docker: Build the Docker image:

- **bash**
  docker-compose build

## Run the application:

- **bash**
  - docker-compose up

**Your application will be available at http://localhost:5000.**

## API Endpoints

- ## Root Route

  - **Try accessing the root route:** `http://localhost:5000`
    - This will return a JSON response:
      ```json
      {
        "msg": "Welcome to Flask-based API's Application"
      }
      ```

- ## Authentication
  - **POST /signup: Register a user.**
  - **POST /login: Login and get JWT token.**
- ## Users
  - **GET /users/: Get all users** (admin only).
  - **GET /users/<user_id>:** Get user by ID (admin only).
  - **PUT /users/<user_id>:** Update user (admin only).
  - **DELETE /users/<user_id>:** Soft-delete user (admin only).
  - **POST /users/batch-delete:** Soft-delete multiple users (admin only).
  - **GET /users/trash:** View soft-deleted users (admin only).
  - **POST /users/restore/<user_id>:** Restore soft-deleted user (admin only).
  - **DELETE /users/trash/<user_id>:** Permanently delete from trash (admin only).
  - **POST /users/promote/<user_id>:** Promote user to admin (admin only).
  - **POST /users/admin/demote/<user_id>:** Demote admin to user (admin only).
- ## Media
  - **POST /media/upload:** Upload an image file using `form-data`.
    - **Key:** `file` (Type: `File`)
    - **Value:** Select an image file from local storage.
    - **Returns:** URL/path of the uploaded file.

### **Important: Directory Setup**

Before using the `/media/upload` endpoint, **you must manually create the following directory** in the project's root folder:

- bash:
  mkdir -p static/media

## Testing

- To run tests for this application, use pytest:

- bash:
  pytest

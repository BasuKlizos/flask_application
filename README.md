User Management API
    A Flask-based API for managing users, including registration, login, and CRUD operations.

Features:
    User registration
    User login (JWT Authentication)
    CRUD operations (Create, Read, Update, Delete)
    User promotion/demotion (admin role)
    Soft-delete and restore users
    Permanent delete from trash

Getting Started:
    Clone the repository:

    bash
        git clone https://github.com/your-username/project-name.git
        cd project-name


Set up a virtual environment:

    bash
        python3 -m venv venv
        
        source venv/bin/activate  # For macOS/Linux
        
        venv\Scripts\activate  # For Windows


Install dependencies:

    bash
        pip install -r requirements.txt

Set up environment variables in a .env file:

.env
    SECRET_KEY=your-secret-key
    JWT_SECRET_KEY=your-jwt-secret-key
    MONGO_USERNAME=your-mongo-username
    MONGO_PASSWORD=your-mongo-password
    MONGO_CLUSTER=your-mongo-cluster-url
    MONGO_DB=your-database-name
    UPLOAD_FOLDER=your-upload-folder-path


Run the application:

bash
    python main.py


Docker:
    Build the Docker image:

bash
    docker-compose build

Run the application:
    bash
        docker-compose up

API Endpoints:
    POST /auth/signup: Register a user.
    POST /auth/login: Login and get JWT token.
    GET /users/: Get all users (admin only).
    GET /users/<user_id>: Get user by ID.
    PUT /users/<user_id>: Update user (admin only).
    DELETE /users/<user_id>: Soft-delete user (admin only).
    POST /users/batch-delete: Soft-delete multiple users (admin only).
    GET /users/trash: View soft-deleted users (admin only).
    POST /users/restore/<user_id>: Restore soft-deleted user.
    DELETE /users/trash/<user_id>: Permanently delete from trash.
    POST /users/promote/<user_id>: Promote user to admin.
    POST /users/admin/demote/<user_id>: Demote admin to user.


Testing:
    Run tests with pytest:

    bash
        pytest
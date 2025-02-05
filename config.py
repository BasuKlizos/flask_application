import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "9e7d55ae37089f065a14f8d6e6e1c782f39212f5")
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "ff1abfbfdad323ad0fcd5a451a24deebbc150f3c"
    )

    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "basudev")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "UcjOArSo3yjUaP6C")
    MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "questerdb.a26wb.mongodb.net")
    MONGO_DB = os.getenv("MONGO_DB", "flask_app")
    MONGO_URI = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{quote_plus(MONGO_CLUSTER)}/{quote_plus(MONGO_DB)}?retryWrites=true&w=majority"

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(
            "C:",
            "Users",
            "Basudev Samanta",
            "Desktop",
            "first_app",
            "flask_app",
            "static",
            "media",
        ),
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

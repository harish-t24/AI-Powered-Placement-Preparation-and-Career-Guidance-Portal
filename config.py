import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "placement_portal_secret_key_2026"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "pdf"
    }

import os

API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    GEMINI_API_KEY = os.getenv(
        "GOOGLE_API_KEY"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
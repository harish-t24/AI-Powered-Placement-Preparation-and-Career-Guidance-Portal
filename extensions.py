from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Database
db = SQLAlchemy()

# Login Manager
login_manager = LoginManager()

# Password Hashing
bcrypt = Bcrypt()
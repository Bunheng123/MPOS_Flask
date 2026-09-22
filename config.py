import os
from datetime import timedelta

class Config:
    # pip install pymysql
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/ssssss"

    SQLALCHEMY_DATABASE_URI = "sqlite:///mydb.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1440)  # session TTL

    # Upload configurations
    UPLOAD_DIR = os.path.join("static", "images", "user")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Module-level shortcuts for convenience
UPLOAD_DIR = Config.UPLOAD_DIR
ALLOWED_EXT = Config.ALLOWED_EXTENSIONS
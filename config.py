import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # Cookie設定
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # RenderではHTTPSなので本番はTrue
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"

    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
class Config:
    SECRET_KEY = 'azde6789hul'  # セッションに必須！
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgre@localhost/azulabdb'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 最大2MB
    DEBUG = False
    # 🔥 メール設定
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'wsxcerty5@gmail.com'
    MAIL_PASSWORD = 'gphhkvbqndmeinfd'  # ←重要

class DevelopmentConfig(Config):
    DEBUG = True

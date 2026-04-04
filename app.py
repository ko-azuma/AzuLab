from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

# Flaskアプリ設定
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
# 画像アップロード先を指定
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
# ディレクトリが存在しなければ作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# DB初期化
db = SQLAlchemy(app)
# ログ設定
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
# アップロード許可拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
#　モデル
from datetime import datetime

class User(db.Model):
    __tablename__ = "usr010"

    usr_id = db.Column(db.String(10), primary_key=True)
    usr_nm = db.Column(db.String(32), nullable=False)
    dlt_flg = db.Column(db.String(1), default='0')

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(10))
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow)

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(10))
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserAuth(db.Model):
    __tablename__ = "usr020"

    usr_id = db.Column(db.String(10), db.ForeignKey('usr010.usr_id'), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)

    login_fail_count = db.Column(db.Integer, default=0)
    account_lock_flg = db.Column(db.String(1), default='0')

    last_login_tmstmp = db.Column(db.DateTime)

    dlt_flg = db.Column(db.String(1), default='0')

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(10))
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow)

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(10))
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(db.Model):
    __tablename__ = "pst010"

    blg_id = db.Column(db.String(10), primary_key=True)
    blg_nm = db.Column(db.String(255), nullable=False)
    blg_img_pt = db.Column(db.String(200))
    blg_ctg = db.Column(db.String(20))
    blg_dtl = db.Column(db.String(1000))
    blg_url = db.Column(db.String(200))

    dlt_flg = db.Column(db.String(1), default='0')

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(10))
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow)

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(10))
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Contact(db.Model):
    __tablename__ = "ctc010"

    ctc_id = db.Column(db.String(10), primary_key=True)
    ctc_nm = db.Column(db.String(255), nullable=False)
    ctc_nm_kn = db.Column(db.String(255))
    ctc_ml = db.Column(db.String(200))
    ctc_hn = db.Column(db.String(20))
    ctc_dtl = db.Column(db.String(1000))

    dlt_flg = db.Column(db.String(1), default='0')

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(10))
    rec_crtn_tmstmp = db.Column(db.DateTime, default=datetime.utcnow)

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(10))
    rec_upd_tmstmp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from datetime import datetime

class PasswordResetToken(db.Model):
    __tablename__ = "pss_rsts010"

    token_id = db.Column(db.String(36), primary_key=True)

    usr_id = db.Column(
        db.String(10),
        db.ForeignKey('usr010.usr_id'),
        nullable=False
    )

    reset_token_hash = db.Column(
        db.String(255),
        unique=True
    )

    token_type = db.Column(db.Integer)  # 0:リセット 1:ロック解除 2:メール認証

    expires_at = db.Column(db.DateTime)

    status = db.Column(db.Integer)  # 0:有効 1:使用済み

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
# ログフォーマット
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logging.info("トップページ表示")
logging.warning("ログイン失敗")
logging.error("DB接続エラー")
# ルート
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/profile")
def profile():
    return "<h1>プロフィール</h1>"

@app.route("/works")
def works():
    return "<h1>作品一覧</h1>"

@app.route("/articles")
def articles():
    return "<h1>記事一覧</h1>"

@app.route("/contact")
def contact():
    return "<h1>お問い合わせ</h1>"

@app.route("/login")
def login():
    return "<h1>ログイン</h1>"
# 初期データ作成
def create_initial_user():
    from werkzeug.security import generate_password_hash

    # 既に存在するかチェック
    existing_user = User.query.filter_by(
        usr_id="k.azuma.atlab@gmail.com"
    ).first()

    if existing_user:
        return

    # USR010
    user = User(
        usr_id="k.azuma.atlab@gmail.com",
        usr_nm="管理者",
        dlt_flg='0',
        rec_crtn_prg_id="INIT",
        rec_crtn_usr_id="SYSTEM"
    )

    # USR020
    auth = UserAuth(
        usr_id="k.azuma.atlab@gmail.com",
        password_hash=generate_password_hash("Azulab7908"),
        login_fail_count=0,
        account_lock_flg='0',
        rec_crtn_prg_id="INIT",
        rec_crtn_usr_id="SYSTEM"
    )

    db.session.add(user)
    db.session.add(auth)
    db.session.commit()
# DB作成時
import os

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Flaskの2重実行防止
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            create_initial_user()

    app.run(debug=True)
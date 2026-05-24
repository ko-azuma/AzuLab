from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv

from functools import wraps
from datetime import datetime, timedelta

import os
import uuid
import hashlib
import logging


# =========================
# 環境変数
# =========================
load_dotenv()

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")


# =========================
# Flask設定
# =========================
app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

app.config["UPLOAD_FOLDER"] = os.path.join(
    os.getcwd(),
    "static",
    "uploads"
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# =========================
# DB
# =========================
db = SQLAlchemy(app)


# =========================
# Mail
# =========================
mail = Mail(app)


# =========================
# ログ
# =========================
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


# =========================
# アップロード
# =========================
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_image(file):

    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = (
        str(uuid.uuid4()) +
        "_" +
        secure_filename(file.filename)
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    return f"uploads/{filename}"


def delete_image(image_path):

    if not image_path:
        return

    filename = os.path.basename(image_path)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)


# =========================
# モデル
# =========================
class User(db.Model):

    __tablename__ = "usr010"

    usr_id = db.Column(
        db.String(255),
        primary_key=True
    )

    usr_nm = db.Column(
        db.String(32),
        nullable=False
    )

    dlt_flg = db.Column(
        db.String(1),
        default='0'
    )

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(255))

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(255))

    rec_upd_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class UserAuth(db.Model):

    __tablename__ = "usr020"

    usr_id = db.Column(
        db.String(255),
        db.ForeignKey("usr010.usr_id"),
        primary_key=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    login_fail_count = db.Column(
        db.Integer,
        default=0
    )

    account_lock_flg = db.Column(
        db.String(1),
        default='0'
    )

    last_login_tmstmp = db.Column(db.DateTime)

    dlt_flg = db.Column(
        db.String(1),
        default='0'
    )

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(255))

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(255))

    rec_upd_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Article(db.Model):

    __tablename__ = "pst010"

    blg_id = db.Column(
        db.String(10),
        primary_key=True
    )

    blg_nm = db.Column(
        db.String(255),
        nullable=False
    )

    blg_img_pt = db.Column(db.String(200))
    blg_ctg = db.Column(db.String(20))
    blg_dtl = db.Column(db.String(1000))
    blg_url = db.Column(db.String(200))

    dlt_flg = db.Column(
        db.String(1),
        default='0'
    )

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(255))

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(255))

    rec_upd_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Work(db.Model):

    __tablename__ = "wrk010"

    wrk_id = db.Column(
        db.String(10),
        primary_key=True
    )

    wrk_nm = db.Column(
        db.String(255),
        nullable=False
    )

    wrk_img_pt = db.Column(db.String(200))
    wrk_ctg = db.Column(db.String(20))
    wrk_dtl = db.Column(db.String(1000))
    wrk_url = db.Column(db.String(200))

    dlt_flg = db.Column(
        db.String(1),
        default='0'
    )

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(255))

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(255))

    rec_upd_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Contact(db.Model):

    __tablename__ = "ctc010"

    ctc_id = db.Column(
        db.String(10),
        primary_key=True
    )

    ctc_nm = db.Column(
        db.String(255),
        nullable=False
    )

    ctc_nm_kn = db.Column(db.String(255))
    ctc_ml = db.Column(db.String(200))
    ctc_hn = db.Column(db.String(20))
    ctc_dtl = db.Column(db.String(1000))

    dlt_flg = db.Column(
        db.String(1),
        default='0'
    )

    rec_crtn_prg_id = db.Column(db.String(50))
    rec_crtn_usr_id = db.Column(db.String(255))

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rec_upd_prg_id = db.Column(db.String(50))
    rec_upd_usr_id = db.Column(db.String(255))

    rec_upd_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class PasswordResetToken(db.Model):

    __tablename__ = "pss_rsts010"

    token_id = db.Column(
        db.String(36),
        primary_key=True
    )

    usr_id = db.Column(
        db.String(255),
        db.ForeignKey("usr010.usr_id"),
        nullable=False
    )

    reset_token_hash = db.Column(
        db.String(255),
        unique=True
    )

    token_type = db.Column(db.Integer)

    expires_at = db.Column(db.DateTime)

    status = db.Column(db.Integer)

    rec_crtn_tmstmp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# ログインチェック
# =========================
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function


# =========================
# メール送信
# =========================
def send_mail(to, subject, body):

    msg = Message(
        subject,
        sender=app.config["MAIL_USERNAME"],
        recipients=[to]
    )

    msg.body = body

    try:
        mail.send(msg)

    except Exception as e:
        logging.error(f"メール送信失敗: {e}")


# =========================
# 初期ユーザ
# =========================
def create_initial_user():

    existing_user = User.query.filter_by(
        usr_id=admin_email
    ).first()

    if existing_user:
        return

    user = User(
        usr_id=admin_email,
        usr_nm="管理者",
        dlt_flg='0',
        rec_crtn_prg_id="INIT",
        rec_crtn_usr_id="SYSTEM"
    )

    auth = UserAuth(
        usr_id=admin_email,
        password_hash=generate_password_hash(
            admin_password
        ),
        login_fail_count=0,
        account_lock_flg='0',
        rec_crtn_prg_id="INIT",
        rec_crtn_usr_id="SYSTEM"
    )

    db.session.add(user)
    db.session.add(auth)

    db.session.commit()


# =========================
# TOP
# =========================
@app.route("/")
def index():

    works = Work.query.filter_by(
        dlt_flg='0'
    ).order_by(
        Work.rec_crtn_tmstmp.desc()
    ).limit(5).all()

    articles = Article.query.filter_by(
        dlt_flg='0'
    ).order_by(
        Article.rec_crtn_tmstmp.desc()
    ).limit(5).all()

    return render_template(
        "index.html",
        works=works,
        articles=articles
    )


# =========================
# 実行
# =========================
if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        if os.environ.get(
            "WERKZEUG_RUN_MAIN"
        ) == "true":

            create_initial_user()

    app.run(debug=True)
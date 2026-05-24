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

    works = Work.query.filter_by(dlt_flg='0') \
        .order_by(Work.rec_crtn_tmstmp.desc()) \
        .limit(5).all()

    articles = Article.query.filter_by(dlt_flg='0') \
        .order_by(Article.rec_crtn_tmstmp.desc()) \
        .limit(5).all()

    return render_template(
        "index.html",
        works=works,
        articles=articles
    )


# =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():
    return render_template("profile.html")


# =========================
# WORKS
# =========================

@app.route("/works")
def works():

    page = request.args.get("page", 1, type=int)

    pagination = Work.query.filter_by(dlt_flg='0') \
        .order_by(Work.rec_crtn_tmstmp.desc()) \
        .paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "works.html",
        works=pagination.items,
        pagination=pagination
    )

# =========================
# ADD WORK
# =========================

@app.route("/works/add", methods=["GET", "POST"])
@login_required
def add_work():

    if request.method == "POST":

        image_path = save_image(
            request.files.get("image")
        )

        work = Work(
            wrk_id=str(uuid.uuid4())[:10],
            wrk_nm=request.form["wrk_nm"],
            wrk_img_pt=image_path,
            wrk_ctg=request.form["wrk_ctg"],
            wrk_dtl=request.form["wrk_dtl"],
            wrk_url=request.form["wrk_url"],
            dlt_flg='0',

            rec_crtn_prg_id="ADD_WORK",
            rec_crtn_usr_id=session.get("user_id"),
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(work)
        db.session.commit()

        flash("作品を追加しました")

        return redirect(url_for("works"))

    return render_template("work_add.html")

@app.route("/works/<string:wrk_id>")
def work_detail(wrk_id):

    work = Work.query.get_or_404(wrk_id)

    return render_template(
        "work_detail.html",
        work=work
    )

@app.route("/works/edit/<string:wrk_id>", methods=["GET", "POST"])
@login_required
def edit_work(wrk_id):

    work = Work.query.get_or_404(wrk_id)

    if request.method == "POST":

        # 画像処理
        file = request.files.get("image")

        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            work.wrk_img_pt = f"uploads/{filename}"

        # テキスト更新
        work.wrk_nm = request.form["wrk_nm"]
        work.wrk_ctg = request.form["wrk_ctg"]
        work.wrk_dtl = request.form["wrk_dtl"]
        work.wrk_url = request.form["wrk_url"]

        db.session.commit()

        return redirect(url_for("works"))

    return render_template("work_edit.html", work=work)

# =========================
# ARTICLES
# =========================

@app.route("/articles")
def articles():

    page = request.args.get("page", 1, type=int)

    pagination = Article.query.filter_by(dlt_flg='0') \
        .order_by(Article.rec_crtn_tmstmp.desc()) \
        .paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "articles.html",
        articles=pagination.items,
        pagination=pagination
    )

# =========================
# ADD ARTICLE
# =========================

@app.route("/articles/add", methods=["GET", "POST"])
@login_required
def add_article():

    if request.method == "POST":

        image_path = save_image(
            request.files.get("image")
        )

        article = Article(
            blg_id=str(uuid.uuid4())[:10],
            blg_nm=request.form["blg_nm"],
            blg_img_pt=image_path,
            blg_ctg=request.form["blg_ctg"],
            blg_dtl=request.form["blg_dtl"],
            blg_url=request.form["blg_url"],
            dlt_flg='0',

            rec_crtn_prg_id="ADD_ARTICLE",
            rec_crtn_usr_id=session.get("user_id"),
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(article)
        db.session.commit()

        flash("記事を追加しました")

        return redirect(url_for("articles"))

    return render_template("article_add.html")

@app.route("/articles/<string:blg_id>")
def article_detail(blg_id):

    article = Article.query.get_or_404(blg_id)

    return render_template(
        "article_detail.html",
        article=article
    )

@app.route("/articles/edit/<string:blg_id>", methods=["GET", "POST"])
@login_required
def edit_article(blg_id):

    article = Article.query.get_or_404(blg_id)

    if request.method == "POST":

        file = request.files.get("image")

        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            article.blg_img_pt = f"uploads/{filename}"

        article.blg_nm = request.form["blg_nm"]
        article.blg_ctg = request.form["blg_ctg"]
        article.blg_dtl = request.form["blg_dtl"]
        article.blg_url = request.form["blg_url"]

        article.rec_upd_usr_id = session.get("user_id")
        article.rec_upd_tmstmp = datetime.utcnow()

        db.session.commit()

        return redirect(url_for("articles"))

    return render_template("article_edit.html", article=article)
# =========================
# CONTACT
# =========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        contact = Contact(
            ctc_id=str(uuid.uuid4())[:10],
            ctc_nm=request.form["ctc_nm"],
            ctc_nm_kn=request.form.get("ctc_nm_kn"),
            ctc_ml=request.form.get("ctc_ml"),
            ctc_hn=request.form.get("ctc_hn"),
            ctc_dtl=request.form.get("ctc_dtl"),
            dlt_flg='0',
            rec_crtn_prg_id="CONTACT",
            rec_crtn_usr_id="GUEST",
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(contact)
        db.session.commit()

        flash("お問い合わせを送信しました")

        return redirect(url_for("index"))

    return render_template("contact.html")

@app.route("/contacts/delete/<string:ctc_id>", methods=["POST"])
@login_required
def delete_contact(ctc_id):
    contact = Contact.query.get_or_404(ctc_id)

    contact.dlt_flg = '1'
    contact.rec_upd_usr_id = session.get("user_id")
    contact.rec_upd_tmstmp = datetime.utcnow()

    db.session.commit()

    return redirect(url_for("dashboard"))

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usr_id = request.form["usr_id"]
        password = request.form["password"]

        user_auth = UserAuth.query.filter_by(
            usr_id=usr_id,
            dlt_flg='0'
        ).first()

        if user_auth:
            is_valid = check_password_hash(
                user_auth.password_hash,
                password
            )
        else:
            check_password_hash(
                generate_password_hash("dummy"),
                password
            )
            is_valid = False

        if user_auth and user_auth.account_lock_flg == '1':
            flash("ユーザーIDまたはパスワードが違います")
            return redirect(url_for("login"))

        if not is_valid:

            if user_auth:
                user_auth.login_fail_count += 1

                if user_auth.login_fail_count >= 5:
                    user_auth.account_lock_flg = '1'

                db.session.commit()

            flash("ユーザーIDまたはパスワードが違います")

            return redirect(url_for("login"))

        user_auth.login_fail_count = 0
        user_auth.last_login_tmstmp = datetime.utcnow()

        session["user_id"] = usr_id

        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
@login_required
def dashboard():

    # 作品一覧
    work_page = request.args.get(
        "work_page",
        1,
        type=int
    )

    work_pagination = Work.query.filter_by(
        dlt_flg='0'
    ).order_by(
        Work.rec_crtn_tmstmp.desc()
    ).paginate(
        page=work_page,
        per_page=20,
        error_out=False
    )

    # 記事一覧
    article_page = request.args.get(
        "article_page",
        1,
        type=int
    )

    article_pagination = Article.query.filter_by(
        dlt_flg='0'
    ).order_by(
        Article.rec_crtn_tmstmp.desc()
    ).paginate(
        page=article_page,
        per_page=20,
        error_out=False
    )

    # お問い合わせ一覧
    contact_page = request.args.get(
        "contact_page",
        1,
        type=int
    )

    contact_pagination = Contact.query.filter_by(
        dlt_flg='0'
    ).order_by(
        Contact.rec_crtn_tmstmp.desc()
    ).paginate(
        page=contact_page,
        per_page=20,
        error_out=False
    )

    return render_template(
        "dashboard.html",
        works=work_pagination.items,
        work_pagination=work_pagination,

        articles=article_pagination.items,
        article_pagination=article_pagination,

        contacts=contact_pagination.items,
        contact_pagination=contact_pagination
    )

# =========================
# CHANGE PASSWORD
# =========================

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_pw = request.form["current_password"]
        new_pw = request.form["new_password"]
        confirm_pw = request.form["confirm_password"]

        # ユーザー取得
        user = UserAuth.query.filter_by(
            usr_id=session.get("user_id"),
            dlt_flg='0'
        ).first()

        if not user:
            flash("ユーザーが存在しません")
            return redirect(url_for("change_password"))

        # 現在パスワード確認
        if not check_password_hash(
            user.password_hash,
            current_pw
        ):
            flash("現在のパスワードが違います")
            return redirect(url_for("change_password"))

        # 新パスワード一致確認
        if new_pw != confirm_pw:
            flash("新しいパスワードが一致しません")
            return redirect(url_for("change_password"))

        # 8文字以上
        if len(new_pw) < 8:
            flash("8文字以上にしてください")
            return redirect(url_for("change_password"))

        # 英数字混在チェック
        if new_pw.isalpha() or new_pw.isdigit():
            flash("英数字を組み合わせてください")
            return redirect(url_for("change_password"))

        # 更新
        user.password_hash = generate_password_hash(new_pw)

        user.rec_upd_usr_id = session.get("user_id")
        user.rec_upd_tmstmp = datetime.utcnow()

        db.session.commit()

        # ログアウト
        session.clear()

        flash("パスワードを変更しました。再ログインしてください。")

        return redirect(url_for("login"))

    return render_template("change_password.html")

# =========================
# PASSWORD RESET REQUEST
# =========================

@app.route("/password_reset_request", methods=["GET", "POST"])
def password_reset_request():

    if request.method == "POST":

        usr_id = request.form["usr_id"]

        user = UserAuth.query.filter_by(
            usr_id=usr_id,
            dlt_flg='0'
        ).first()

        if user:

            raw_token = str(uuid.uuid4())

            token_hash = hashlib.sha256(
                raw_token.encode()
            ).hexdigest()

            token = PasswordResetToken(
                token_id=str(uuid.uuid4()),
                usr_id=usr_id,
                reset_token_hash=token_hash,
                token_type=0,
                expires_at=datetime.utcnow() + timedelta(hours=1),
                status=0
            )

            db.session.add(token)
            db.session.commit()

            reset_link = f"http://localhost:5000/reset_password/{raw_token}"

            send_mail(
                usr_id,
                "パスワードリセット",
                f"以下のリンクから再設定してください\n{reset_link}"
            )

        flash("メールを送信しました")

        return redirect(url_for("reset_request_done"))

    return render_template("password_reset_request.html")


@app.route("/reset_request_done")
def reset_request_done():

    return render_template("reset_request_done.html")


# =========================
# RESET PASSWORD
# =========================

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    token_data = PasswordResetToken.query.filter_by(
        reset_token_hash=token_hash,
        token_type=0,
        status=0
    ).first()

    if not token_data:
        flash("無効なリンクです")
        return redirect(url_for("login"))

    if token_data.expires_at < datetime.utcnow():
        flash("リンクの有効期限が切れています")
        return redirect(url_for("login"))

    user = UserAuth.query.filter_by(
        usr_id=token_data.usr_id,
        dlt_flg='0'
    ).first()

    if not user:
        flash("ユーザーが存在しません")
        return redirect(url_for("login"))

    if request.method == "POST":

        new_pw = request.form["new_password"]
        confirm_pw = request.form["confirm_password"]

        if new_pw != confirm_pw:
            flash("パスワードが一致しません")
            return redirect(request.url)

        if len(new_pw) < 8:
            flash("8文字以上にしてください")
            return redirect(request.url)

        if new_pw.isdigit() or new_pw.isalpha():
            flash("英数字を組み合わせてください")
            return redirect(request.url)

        user.password_hash = generate_password_hash(new_pw)

        user.login_fail_count = 0
        user.account_lock_flg = '0'

        token_data.status = 1

        db.session.commit()

        flash("パスワードを再設定しました")

        return redirect(url_for("login"))

    return render_template(
        "reset_password.html"
    )
# =========================
# UNLOCK REQUEST
# =========================

@app.route("/unlock_request", methods=["GET", "POST"])
def unlock_request():

    if request.method == "POST":

        usr_id = request.form["usr_id"]

        user = UserAuth.query.filter_by(
            usr_id=usr_id,
            dlt_flg='0'
        ).first()

        # 存在する場合のみメール送信
        if user:

            # 生トークン
            raw_token = str(uuid.uuid4())

            # DB保存用ハッシュ
            token_hash = hashlib.sha256(
                raw_token.encode()
            ).hexdigest()

            # トークン保存
            token = PasswordResetToken(
                token_id=str(uuid.uuid4()),
                usr_id=usr_id,
                reset_token_hash=token_hash,
                token_type=1,  # 1 = ロック解除
                expires_at=datetime.utcnow() + timedelta(hours=1),
                status=0
            )

            db.session.add(token)
            db.session.commit()

            # ロック解除URL
            unlock_link = (
                f"http://localhost:5000/"
                f"unlock_account/{raw_token}"
            )

            # メール送信
            send_mail(
                usr_id,
                "アカウントロック解除",
                f"以下のリンクから解除してください\n{unlock_link}"
            )

        # ユーザー存在有無を隠す
        flash(
            "メールを送信しました"
            "（該当するアカウントが存在する場合）"
        )

        return redirect(
            url_for("unlock_request_done")
        )

    return render_template(
        "unlock_request.html"
    )


# =========================
# UNLOCK REQUEST DONE
# =========================

@app.route("/unlock_request_done")
def unlock_request_done():

    return render_template(
        "unlock_request_done.html"
    )


# =========================
# UNLOCK ACCOUNT
# =========================

@app.route("/unlock_account/<token>")
def unlock_account(token):

    # トークンハッシュ化
    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    # トークン取得
    token_data = PasswordResetToken.query.filter_by(
        reset_token_hash=token_hash,
        token_type=1,
        status=0
    ).first()

    # 無効
    if not token_data:
        flash("無効なリンクです")
        return redirect(url_for("login"))

    # 有効期限切れ
    if token_data.expires_at < datetime.utcnow():
        flash("リンクの有効期限が切れています")
        return redirect(url_for("login"))

    # ユーザー取得
    user = UserAuth.query.filter_by(
        usr_id=token_data.usr_id,
        dlt_flg='0'
    ).first()

    # ユーザー不存在
    if not user:
        flash("ユーザーが存在しません")
        return redirect(url_for("login"))

    # ロック解除
    user.account_lock_flg = '0'
    user.login_fail_count = 0

    # トークン使用済み
    token_data.status = 1

    db.session.commit()

    flash(
        "アカウントロックを解除しました。"
        "ログインしてください。"
    )

    return redirect(url_for("login"))

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
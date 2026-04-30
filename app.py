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

class Work(db.Model):
    __tablename__ = "wrk010"

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

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
# ルート
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():

    works = Work.query.filter_by(dlt_flg='0') \
        .order_by(Work.rec_crtn_tmstmp.desc()) \
        .limit(5).all()

    articles = Article.query.filter_by(dlt_flg='0') \
        .order_by(Article.rec_crtn_tmstmp.desc()) \
        .limit(5).all()

    return render_template("index.html", works=works, articles=articles)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/works")
def works():
    page = request.args.get("page", 1, type=int)

    pagination = Work.query.filter_by(dlt_flg='0') \
        .order_by(Work.rec_crtn_tmstmp.desc()) \
        .paginate(page=page, per_page=20)

    works = pagination.items

    return render_template(
        "works.html",
        works=works,
        pagination=pagination
    )

@app.route("/works/<string:wrk_id>")
def work_detail(wrk_id):
    work = Work.query.get_or_404(wrk_id)
    return render_template("work_detail.html", work=work)

@app.route("/articles")
def articles():
    return "<h1>記事一覧</h1>"

import uuid
from datetime import datetime

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        ctc_id = str(uuid.uuid4())[:10]

        contact = Contact(
            ctc_id=ctc_id,
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

        return redirect(url_for("top"))

    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usr_id = request.form["usr_id"]
        password = request.form["password"]

        # 認証テーブル（USR020）
        user_auth = UserAuth.query.filter_by(
            usr_id=usr_id,
            dlt_flg='0'
        ).first()

        if not user_auth:
            flash("ユーザーが存在しません")
            return redirect(url_for("login"))

        # ロックチェック
        if user_auth.account_lock_flg == '1':
            flash("アカウントがロックされています")
            return redirect(url_for("login"))

        # パスワードチェック
        if not check_password_hash(user_auth.password_hash, password):
            user_auth.login_fail_count += 1

            # 5回失敗でロック
            if user_auth.login_fail_count >= 5:
                user_auth.account_lock_flg = '1'
                flash("ログイン失敗が多いためロックしました")

            db.session.commit()

            flash("パスワードが違います")
            return redirect(url_for("login"))

        # 成功時
        user_auth.login_fail_count = 0
        user_auth.last_login_tmstmp = datetime.utcnow()

        db.session.commit()

        # セッション保存
        session["user_id"] = usr_id

        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

import uuid
from datetime import datetime, timedelta
import hashlib

@app.route("/password_reset_request", methods=["GET", "POST"])
def password_reset_request():

    if request.method == "POST":
        usr_id = request.form["usr_id"]

        # ユーザ存在確認
        user = UserAuth.query.filter_by(usr_id=usr_id, dlt_flg='0').first()

        if not user:
            flash("ユーザーが存在しません")
            return redirect(url_for("password_reset_request"))

        # トークン生成
        raw_token = str(uuid.uuid4())
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        token = PasswordResetToken(
            token_id=str(uuid.uuid4()),
            usr_id=usr_id,
            reset_token_hash=token_hash,
            token_type=0,  # パスワードリセット
            expires_at=datetime.utcnow() + timedelta(hours=1),
            status=0,
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(token)
        db.session.commit()

        # 本来はここでメール送信
        print(f"リセットリンク: /reset_password/{raw_token}")

        return redirect(url_for("reset_request_done"))

    return render_template("password_reset_request.html")

@app.route("/reset_request_done")
def reset_request_done():
    return render_template("reset_request_done.html")

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    import hashlib
    from datetime import datetime

    token_hash = hashlib.sha256(token.encode()).hexdigest()

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

        # 🔥 更新
        user.password_hash = generate_password_hash(new_pw)
        user.login_fail_count = 0
        user.account_lock_flg = '0'

        token_data.status = 1

        db.session.commit()

        flash("パスワードを再設定しました。ログインしてください。")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/unlock_request", methods=["GET", "POST"])
def unlock_request():

    if request.method == "POST":
        usr_id = request.form["usr_id"]

        user = UserAuth.query.filter_by(usr_id=usr_id, dlt_flg='0').first()

        if not user:
            flash("ユーザーが存在しません")
            return redirect(url_for("unlock_request"))

        raw_token = str(uuid.uuid4())
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        token = PasswordResetToken(
            token_id=str(uuid.uuid4()),
            usr_id=usr_id,
            reset_token_hash=token_hash,
            token_type=1,  # ロック解除
            expires_at=datetime.utcnow() + timedelta(hours=1),
            status=0,
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(token)
        db.session.commit()

        print(f"ロック解除リンク: /unlock_account/{raw_token}")

        return redirect(url_for("unlock_request_done"))
    return render_template("unlock_request.html")

@app.route("/unlock_request_done")
def unlock_request_done():
    return render_template("unlock_request_done.html")

@app.route("/unlock_account/<token>")
def unlock_account(token):

    import hashlib
    from datetime import datetime

    # トークンをハッシュ化（DBと照合）
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    token_data = PasswordResetToken.query.filter_by(
        reset_token_hash=token_hash,
        token_type=1,   # ロック解除
        status=0
    ).first()

    # トークン存在チェック
    if not token_data:
        flash("無効なリンクです")
        return redirect(url_for("login"))

    # 有効期限チェック
    if token_data.expires_at < datetime.utcnow():
        flash("リンクの有効期限が切れています")
        return redirect(url_for("login"))

    # ユーザ取得
    user = UserAuth.query.filter_by(
        usr_id=token_data.usr_id,
        dlt_flg='0'
    ).first()

    if not user:
        flash("ユーザーが存在しません")
        return redirect(url_for("login"))

    # 🔥 ロック解除
    user.account_lock_flg = '0'
    user.login_fail_count = 0

    # トークン使用済みにする
    token_data.status = 1

    db.session.commit()

    flash("アカウントロックを解除しました。ログインしてください。")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():

    # 作品ページ
    work_page = request.args.get("work_page", 1, type=int)
    work_pagination = Work.query.filter_by(dlt_flg='0') \
        .order_by(Work.rec_crtn_tmstmp.desc()) \
        .paginate(page=work_page, per_page=20)

    # 記事ページ
    article_page = request.args.get("article_page", 1, type=int)
    article_pagination = Article.query.filter_by(dlt_flg='0') \
        .order_by(Article.rec_crtn_tmstmp.desc()) \
        .paginate(page=article_page, per_page=20)

    # 問い合わせページ
    contact_page = request.args.get("contact_page", 1, type=int)
    contact_pagination = Contact.query.filter_by(dlt_flg='0') \
        .order_by(Contact.rec_crtn_tmstmp.desc()) \
        .paginate(page=contact_page, per_page=20)

    return render_template(
        "dashboard.html",
        works=work_pagination.items,
        work_pagination=work_pagination,
        articles=article_pagination.items,
        article_pagination=article_pagination,
        contacts=contact_pagination.items,
        contact_pagination=contact_pagination
    )

@app.route("/works/delete/<string:wrk_id>", methods=["POST"])
@login_required
def delete_work(wrk_id):
    work = Work.query.get_or_404(wrk_id)

    work.dlt_flg = '1'
    work.rec_upd_usr_id = session.get("user_id")
    work.rec_upd_tmstmp = datetime.utcnow()

    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/articles/delete/<string:blg_id>", methods=["POST"])
@login_required
def delete_article(blg_id):
    article = Article.query.get_or_404(blg_id)

    article.dlt_flg = '1'
    article.rec_upd_usr_id = session.get("user_id")
    article.rec_upd_tmstmp = datetime.utcnow()

    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/contacts/delete/<string:ctc_id>", methods=["POST"])
@login_required
def delete_contact(ctc_id):
    contact = Contact.query.get_or_404(ctc_id)

    contact.dlt_flg = '1'
    contact.rec_upd_usr_id = session.get("user_id")
    contact.rec_upd_tmstmp = datetime.utcnow()

    db.session.commit()

    return redirect(url_for("dashboard"))

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":
        current_pw = request.form["current_password"]
        new_pw = request.form["new_password"]
        confirm_pw = request.form["confirm_password"]

        # ユーザ取得
        user = UserAuth.query.filter_by(
            usr_id=session.get("user_id"),
            dlt_flg='0'
        ).first()

        if not user:
            flash("ユーザーが存在しません")
            return redirect(url_for("change_password"))

        # 現在パスワードチェック
        if not check_password_hash(user.password_hash, current_pw):
            flash("現在のパスワードが違います")
            return redirect(url_for("change_password"))

        # 一致チェック
        if new_pw != confirm_pw:
            flash("新しいパスワードが一致しません")
            return redirect(url_for("change_password"))

        # 🔥 ① パスワード強度チェック
        if len(new_pw) < 8:
            flash("パスワードは8文字以上にしてください")
            return redirect(url_for("change_password"))

        if new_pw.isdigit() or new_pw.isalpha():
            flash("英数字を組み合わせてください")
            return redirect(url_for("change_password"))

        # 更新
        user.password_hash = generate_password_hash(new_pw)
        user.rec_upd_usr_id = session.get("user_id")
        user.rec_upd_tmstmp = datetime.utcnow()

        db.session.commit()

        # 🔥 ② 強制ログアウト
        session.clear()

        flash("パスワードを変更しました。再ログインしてください。")
        return redirect(url_for("login"))

    return render_template("change_password.html")

@app.route("/articles/add", methods=["GET", "POST"])
@login_required
def add_article():

    if request.method == "POST":

        file = request.files.get("image")
        filename = None

        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        blg_id = str(uuid.uuid4())[:10]

        article = Article(
            blg_id=blg_id,
            blg_nm=request.form["blg_nm"],
            blg_img_pt=f"uploads/{filename}" if filename else None,
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

        return redirect(url_for("articles"))

    return render_template("article_add.html")

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

import uuid
from datetime import datetime

@app.route("/works/add", methods=["GET", "POST"])
def add_work():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        wrk_id = str(uuid.uuid4())[:10]  # 簡易ID生成

        work = Work(
            wrk_id=wrk_id,
            wrk_nm=request.form["wrk_nm"],
            wrk_ctg=request.form["wrk_ctg"],
            wrk_dtl=request.form["wrk_dtl"],
            wrk_url=request.form["wrk_url"],
            dlt_flg='0',
            rec_crtn_prg_id="ADD_WORK",
            rec_crtn_usr_id=session.get("user_id", "SYSTEM"),
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(work)
        db.session.commit()

        return redirect(url_for("works"))

    return render_template("work_add.html")

@app.route("/works/add", methods=["GET", "POST"])
@login_required
def add_work():
    if request.method == "POST":

        file = request.files.get("image")
        filename = None

        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        wrk_id = str(uuid.uuid4())[:10]

        work = Work(
            wrk_id=wrk_id,
            wrk_nm=request.form["wrk_nm"],
            wrk_img_pt=f"uploads/{filename}" if filename else None,
            wrk_ctg=request.form["wrk_ctg"],
            wrk_dtl=request.form["wrk_dtl"],
            wrk_url=request.form["wrk_url"],
            dlt_flg='0',
            rec_crtn_prg_id="ADD_WORK",
            rec_crtn_usr_id=session.get("user_id", "SYSTEM"),
            rec_crtn_tmstmp=datetime.utcnow()
        )

        db.session.add(work)
        db.session.commit()

        return redirect(url_for("works"))

    return render_template("work_add.html")

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
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message

from exts import mail, cache, db
from forms.user import RegisterForm, LoginForm
from models.user import UserModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("user.register"))


@bp.route("/mail/captcha")
def mail_captcha():
    # 验证码信息
    email = request.args.get("mail")
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    captcha = "".join(random.sample(digits, 6))
    body = f"[郁金香博客]您的注册验证码是：{captcha},请勿告诉别人,验证码有效时间：5分钟"
    message = Message(subject="郁金香博客", recipients=[email], body=body)
    mail.send(message)
    cache.set(email, captcha, timeout=300)
    return "验证码发送成功"


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        print("001")
        return render_template("front/login.html")
    else:
        print("002")
        form = LoginForm(request.form)
        if form.validate():
            print("003")
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if user and user.check_password(password):
                print("004")
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("006")
                flash("邮箱或密码错误")
                return redirect(url_for("user.login"))
        else:
            print("007")
            for message in form.messages:
                flash(message)
            return render_template("front/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

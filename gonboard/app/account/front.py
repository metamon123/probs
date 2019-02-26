from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from .forms import RegisterForm, LoginForm, MypageForm
from app import login_manager, db_session

account_bp = Blueprint("account", __name__, template_folder='templates')
login_manager.login_view = "account.login"


@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(uid=uid).first()


@account_bp.route("/")
def index():
    return render_template("main.html")


@account_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(uid=form.uid.data).first():
            msg = f"{form.uid.data} already exists"
            print(msg)
            return msg
        user = User(form.uid.data, form.upw.data,
                    form.msg.data, form.email.data)
        db_session.add(user)
        db_session.commit()
        msg = f"register success, {user.uid}"
        print(msg)
        flash(msg)
        return redirect(request.args.get('next') or url_for('account.index'))
    return render_template('register.html', form=form)


@account_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        msg = ""
        user = User.query.filter_by(uid=form.uid.data).first()
        if user is None:
            msg = f"No such user : {user.uid}"
        if not user.check_password(form.upw.data):
            msg = f"Wrong password"
        if msg == "":
            msg = f"login success, {user.uid}"
            print(msg)
            flash(msg)            
            login_user(user)
            return redirect(request.args.get('next') or url_for('account.index'))
        flash(msg)
        return redirect(request.args.get('next') or url_for('account.login'))
    return render_template("login.html", form=form)


@account_bp.route("/logout", methods=['GET'])
@login_required
def logout():
    flash("logout success")
    logout_user()
    return redirect(request.args.get('next') or url_for('account.login'))


@account_bp.route("/mypage", methods=['GET', 'POST'])
@login_required
def mypage():
    form = MypageForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.new_upw.data != "":
            current_user.set_password(form.new_upw.data)
        if form.msg.data != current_user.msg:
            current_user.msg = form.msg.data
        db_session.commit()
        flash("update success")
        return redirect(request.args.get('next') or url_for('account.index'))
    return render_template("mypage.html", form=form)

#!/usr/bin/env python3
# if it's too dirty, visit /show_m3_7h3_c0d3 for cleaner app.py
from flask import Flask, render_template, request, url_for, session, flash, redirect, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os, re, string, random
import requests as r

from config import secret_key
from database import init_db, db_session
from models import User, Scrap

app = Flask(__name__)
app.secret_key = secret_key


def random_string_generator(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])

def get_user(uid, upw=""):
    if upw == "":
        return db_session.query(User).filter(f"id='{uid}'").all()
    else:
        users = db_session.query(User).filter(f"id='{uid}'").all()
        return [user for user in users if check_password_hash(user.pw, upw)]


# For hacker who has already leaked the source code but is suffering with the python code without newline
@app.route("/show_m3_7h3_c0d3")
def code_leak():
    self = open(__file__)
    src = self.read()
    self.close()
    res = make_response(src)
    res.headers["Content-Type"] = "text/plain"
    return res

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/scrap", methods=["POST"])
def scrap():
    if not "id" in session:
        flash("You've not logged in")
        return redirect("/")

    url = request.form.get("url", "")
    title = request.form.get("title", "No title")

    if url == "":
        flash("Not a good url... hmm...")
        return redirect(url_for("index"))

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    try:
        # Some website needs normal user-agent
        res = r.get(url, headers={"User-Agent" : session['browser']})
    except:
        flash("Not a good url... hmm...")
        return redirect(url_for("index"))

    # download scrapped html source
    fname = "scrap_" + random_string_generator(16)
    f = open(f"scraps/{fname}", 'w', encoding='utf-8')
    f.write(res.text)
    f.close()

    scrap = Scrap(session["id"], fname, title)
    db_session.add(scrap)
    db_session.commit()

    flash(f"Your scrap is stored successfully")
    return redirect(url_for("index"))

@app.route("/view", methods=["GET"])
def view():
    if not "id" in session:
        flash("You've not logged in")
        return redirect(url_for("login"))

    if not "name" in request.args:
        return "name argument is required"

    fname = request.args["name"]
    html = open(f"scraps/{fname}", "r", encoding='utf-8').read()
    res = make_response(html)
    res.headers['Content-Type'] = "text/html; charset=utf-8"
    return res

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        uid = request.form.get("id", "")
        upw = request.form.get("pw", "")

        # non-valid cases
        if uid == "" or upw == "":
            flash("Not a valid id / pw")
            return redirect(url_for("register"))

        if not re.match("^[a-zA-Z0-9]+$", uid):
            flash("Only alphanumeric characters are allowed as id")
            return redirect(url_for("register"))

        if len(get_user(uid)) > 0:
            flash(f'User {uid} already exists')
            return redirect(url_for("login"))

        pwhash = generate_password_hash(upw)
        user = User(uid, pwhash)
        db_session.add(user)
        db_session.commit()
        flash("You were successfully registered")
        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "id" in session:
        flash(f"{session['id']}, you've already logged in.")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        uid = request.form.get("id", "")
        upw = request.form.get("pw", "")

        # non-valid cases
        if uid == "" or upw == "":
            flash("Not a valid id / pw")
            return redirect(url_for("login"))

        if not re.match("^[a-zA-Z0-9]+$", uid):
            flash("Only alphanumeric characters are allowed as id")
            return redirect(url_for("login"))

        users = get_user(uid, upw)
        if len(users) < 1:
            flash("No such user")
            return redirect(url_for("login"))
        if len(users) > 1:
            flash("It's weird... report to the admin")
            return redirect(url_for("login"))

        user = users[0]
        session['id'] = user.id
        session['browser'] = request.headers["User-Agent"]

        flash(f"Welcome {user.id}")
        return redirect(url_for("index"))

@app.route("/mypage")
def mypage():
    if not "id" in session:
        flash("You've not logged in yet")
        return redirect(url_for("login"))

    scraps = db_session.query(Scrap).filter(f"owner_id='{session['id']}'").all()
    return render_template("mypage.html", scraps=scraps)


@app.route("/logout")
def logout():
    if not "id" in session:
        flash("You've not logged in yet")
        return redirect(url_for("index"))

    session.pop("id")
    flash("Bye")
    return redirect(url_for("index"))


def start(port):
    init_db()
    try:
        app.run(debug=True,host='0.0.0.0', port=port)
    finally:
        print("Closing DB...")
        db_session.remove()

if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        port = int(argv[1])
    else:
        port = 30039
    start(port)

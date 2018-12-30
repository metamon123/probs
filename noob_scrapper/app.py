#!/usr/bin/env python3
from flask import Flask, render_template, request, url_for, session, flash, redirect, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests as r

from misc import argcheck, random_string_generator
from config import secret_key
from database import init_db, db_session
from models import User, Scrap

app = Flask(__name__)
app.secret_key = secret_key

scraps_dir = "templates/scraps"

def get_user(uid, upw=""):
    if upw == "":
        return db_session.query(User).filter(User.id==uid).all()
    else:
        users = db_session.query(User).filter(User.id==uid).all()
        return [user for user in users if check_password_hash(user.pw, upw)]

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

        if not (os.path.exists(f"{scraps_dir}/{session['id']}") and os.path.isdir(f"{scraps_dir}/{session['id']}")):
            os.mkdir(f"{scraps_dir}/{session['id']}")

        # download scrapped html source
        fname = "scrap_" + random_string_generator(16)
        f = open(f"{scraps_dir}/{session['id']}/{fname}", 'w')
        f.write(res.text)
        f.close()

        scrap = Scrap(session["id"], fname, title)
        db_session.add(scrap)
        db_session.commit()

        flash(f"Your scrap is stored successfully")
        return redirect(url_for("index"))
    except:
        flash("Not a good url... hmm...")
        return redirect(url_for("index"))

@app.route("/view", methods=["GET"])
def view():
    if not "id" in session:
        flash("You've not logged in")
        return redirect(url_for("login"))

    if not "name" in request.args:
        return "name argument is required"

    uid = session["id"]
    fname = request.args["name"]
    html = open(f"{scraps_dir}/{uid}/{fname}", "r").read()
    res = make_response(html)
    #res.headers['Content-Type'] = "text/html; charset=utf-8"
    return res

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        uid = request.form.get("id", "")
        upw = request.form.get("pw", "")
        if uid == "" or upw == "":
            flash("Not a valid id / pw")
            return redirect(url_for("register"))

        if len(get_user(uid)) > 0:
            flash(f"User id {uid} already exists")
            return redirect(url_for("register"))

        pwhash = generate_password_hash(upw)
        user = User(uid, pwhash)
        db_session.add(user)
        db_session.commit()
        flash("You were successfully registered")
        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "id" in session:
        flash("You've already logged in")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        uid = request.form.get("id", "")
        upw = request.form.get("pw", "")
        if uid == "" or upw == "":
            flash("Not a valid id / pw")
            return redirect(url_for("index"))
    
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

    scraps = db_session.query(Scrap).filter(Scrap.owner_id==session['id']).all()
    return render_template("mypage.html", scraps=scraps)


@app.route("/logout")
def logout():
    if not "id" in session:
        flash("You've not logged in yet")
        return redirect(url_for("index"))

    session.pop("id")
    flash("Bye")
    return redirect(url_for("index"))


if __name__ == "__main__":
    args = argcheck()
    port = 30039
    if args.p != None and args.p > 0 and args.p < 65536:
        port = args.p
    init_db()
    try:
        app.run(debug=True,host='0.0.0.0', port=port)
    finally:
        print("Closing DB...")
        db_session.remove()

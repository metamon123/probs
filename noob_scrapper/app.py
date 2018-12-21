from flask import Flask, render_template, request, url_for, session, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import os, string
import requests as r
import argparse


from config import secret_key
from database import init_db
from database import db_session
from models import User

app = Flask(__name__)
app.secret_key = secret_key

def random_string_generator(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])

def save_response(res):
    '''
    try:
        tempfile.tempdir = "./scraps"
        temp = tempfile.NamedTemporaryFile(prefix="scrap_")
        temp.write(res.text)
        return temp
    except:
        temp.close()
        return None
    '''
    fname = random_string_generator(32)
    f = open("scrap_" + fname, 'w')
    f.write(res.text)
    f.close()

def get_user(uid, upw=""):
    if upw == "":
        return db_session.query(User).filter(User.id==uid).all()
    else:
        users = db_session.query(User).filter(User.id==uid).all()
        for user in users:
            if check_password_hash(user.pw, upw):
                return [user]
        return []

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/scrap", methods=["GET", "POST"])
def scrap():
    if request.method == "GET":
        return "Hi! What do you want to get?"
    elif request.method == "POST":
        url = request.form["url"] if "url" in request.form else ""
        # print(f"request.url : {request.url} / request.path : {request.path}")
        # request.url : http://143.248.2.130:8080/scrap / request.path : /scrap

        pages = []
        if url != "":
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "http://" + url

            try:
                res = r.get(url)
                #print(f"Response of {url} : ")
                #print(res.text)
                pages.append({'url' : url})
            except:
                return "Not a good url... hmm..."

        return render_template("show.html", pages=pages)

@app.route("/scraps/<uid>/<path:subpath>")
def view(uid, subpath):
    print(f"uid : {uid} / subpath : {subpath}")
    return "Not Implemented"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        uid = request.form['id']
        upw = request.form['pw']
        if uid == "" or upw == "":
            flash("Not a valid id / pw")
            return redirect(url_for("register"), code=302)

        pwhash = generate_password_hash(upw)

        if len(get_user(uid)) > 0:
            flash(f"User id {uid} already exists")
            return redirect(url_for("register"), code=302)

        user = User(uid, pwhash)
        db_session.add(user)
        db_session.commit()
        flash("You were successfully registered")
        return redirect(url_for("index"), code=302)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "id" in session:
        flash("You've already logged in")
        return redirect(url_for("index"), code=302)

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        uid = request.form['id']
        upw = request.form['pw']
        if uid == "" or upw == "":
            return "Not a valid id / pw"
        
        users = get_user(uid, upw)
        if len(users) < 1:
            flash("No such user")
            return redirect(url_for("login"), code=302)
        if len(users) > 1:
            flash("It's weird... report to the admin")
            return redirect(url_for("login"), code=302)

        user = users[0]
        session['id'] = user.id
        
        flash(f"Welcome {user.id}")
        return redirect(url_for("index"), code=302)

@app.route("/logout")
def logout():
    if not "id" in session:
        flash("You've not logged in yet")
        return redirect(url_for("index"), code=302)

    session.pop("id")
    flash("Bye")
    return redirect(url_for("index"), code=302)


def argcheck():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="port of the server", type=int)
    args = parser.parse_args()
    return args

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

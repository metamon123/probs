from flask import Flask, render_template, request, url_for, session
from werkzeug.security import generate_password_hash
import string
import os
import requests as r
import argparse

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/scrap", methods = ["GET", "POST"])
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

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uid = request.form['id']
        upw = request.form['pw']
        if uid == "" or upw == "":
            return "Not a valid id / pw"
        
        pwhash = generate_password_hash(upw)
        return f"Your id : {uid} / Your hash(pw) : {pwhash}"
    else:
        return "Wrong request method"

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
    app.run(debug=True,host='0.0.0.0', port=port)

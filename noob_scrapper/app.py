from flask import Flask, render_template, request, url_for
import requests as r
import argparse

app = Flask(__name__)

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

        if url != "":
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "http://" + url

            try:
                res = r.get(url)
                print(f"Response of {url} : ")
                print(res.text)
            except:
                return "Not a good url... hmm..."

            #return render_template("show.html")
        return f"Your url : '{url}'"

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        return "login not yet implemented.. Sorry!"
    else:
        return "Wrong request method"

def argcheck():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="port of the server", type=int)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = argcheck()
    port = 8080
    if args.p != None and args.p > 0 and args.p < 65536:
        port = args.p
    app.run(debug=True,host='0.0.0.0', port=port)

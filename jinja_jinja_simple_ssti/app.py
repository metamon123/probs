from flask import Flask, render_template_string, request, make_response


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    template = request.args.get("t", "")
    if template == "":
        return "Visit /source for original source file"

    # I heard that every server-side template injection payloads contain {{, so I banned it :)
    if "{{" in template:
        return "No Hack"

    return render_template_string(template)

@app.route("/source")
def source():
    src = open(__file__).read()
    res = make_response(src)
    res.headers['Content-Type'] = 'text/plain'
    return res
    

if __name__ == "__main__":
    app.run(debug=1, host="0.0.0.0", port=8080) 

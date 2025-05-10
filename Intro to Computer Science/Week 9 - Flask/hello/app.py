from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


#if "name" in request.args:
#    name = request.args["name"]
#else:
#    name = "world"
#This is a bit clunky, so we use something else instead VVV
#name = request.args.get("name", "world")

@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return render_template("greet.html", name=name)
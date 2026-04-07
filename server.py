from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "secret"

users = {}
patients = [{"id": i, "name": f"Пациент {i}"} for i in range(1, 2001)]
alliances = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        users[login] = {
            "password": password,
            "coins": 1000,
            "diamonds": 100,
            "xp": 0,
            "level": 1
        }
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if login in users and users[login]["password"] == password:
            session["user"] = login
            return redirect("/game")
    return render_template("login.html")

@app.route("/game")
def game():
    if "user" not in session:
        return redirect("/login")

    user = users[session["user"]]
    online = len(users)

    return render_template("game.html", user=user, online=online)

@app.route("/wards")
def wards():
    return render_template("wards.html", patients=patients)

@app.route("/operating")
def operating():
    dice = random.randint(1,6)
    return render_template("operating.html", dice=dice)

@app.route("/lab")
def lab():
    return render_template("lab.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/alliances", methods=["GET","POST"])
def alliances_page():
    if request.method == "POST":
        name = request.form["name"]
        user = users[session["user"]]

        if user["diamonds"] >= 500:
            user["diamonds"] -= 500
            alliances.append(name)

    return render_template("alliances.html", alliances=alliances)

app.run(host="0.0.0.0", port=5000)

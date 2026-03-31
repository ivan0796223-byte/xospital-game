from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "secret"

users = {}
online_players = 5

patients = [{"id": i, "name": f"Пациент {i}"} for i in range(1, 2001)]

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# ---------------- АВТОРИЗАЦИЯ ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if login in users and users[login]["password"] == password:
            session["user"] = login
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        users[login] = {
            "password": password,
            "coins": 1000,
            "diamonds": 500,
            "exp": 0,
            "level": 1
        }

        return redirect("/login")

    return render_template("register.html")

# ---------------- ОСНОВА ----------------

@app.route("/dashboard")
def dashboard():
    user = users[session["user"]]
    return render_template("dashboard.html", user=user, online=online_players)


@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients)


@app.route("/operating")
def operating():
    result = random.randint(1, 6)
    return render_template("operating.html", dice=result)


@app.route("/lab")
def lab():
    return render_template("lab.html")


@app.route("/garage")
def garage():
    return render_template("garage.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/alliance", methods=["GET", "POST"])
def alliance():
    message = ""
    if request.method == "POST":
        if users[session["user"]]["diamonds"] >= 500:
            users[session["user"]]["diamonds"] -= 500
            message = "Союз создан!"
        else:
            message = "Недостаточно алмазов!"
    return render_template("alliance.html", message=message)


@app.route("/doctor")
def doctor():
    return render_template("doctor.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)

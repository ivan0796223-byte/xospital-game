from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "xospital_v3"

users = {}

# ---- 2000 пациентов ----
patients = [{"id": i, "name": f"Пациент {i}", "status": "палата"} for i in range(1, 2001)]

# ---- init игрок ----
def init():
    if "data" not in session:
        session["data"] = {
            "coins": 500,
            "diamonds": 200,
            "exp": 0,
            "level": 1
        }

# ---- HOME ----
@app.route("/")
def home():
    return redirect("/login")

# ---- REGISTER ----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["login"]] = request.form["password"]
        return redirect("/login")
    return render_template("register.html")

# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["login"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            init()
            return redirect("/dashboard")

    return render_template("login.html")

# ---- DASHBOARD ----
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    init()
    data = session["data"]

    return render_template(
        "dashboard.html",
        user=session["user"],
        data=data,
        patients=random.sample(patients, 10),
        online=random.randint(1, 25)
    )

# ---- PATIENTS ----
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:100])

# ---- CALL PATIENT ----
@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Пациент {pid} вызван"

# ---- OPERATING (dice) ----
@app.route("/operate")
def operate():
    dice = random.randint(1, 6)
    return f"🎲 Операция результат: {dice}"

# ---- LAB ----
@app.route("/lab")
def lab():
    return f"🧪 Исследование: {random.choice(['кровь','МРТ','рентген','анализ'])}"

# ---- ALLIANCE ----
@app.route("/alliance")
def alliance():
    init()
    d = session["data"]

    if d["diamonds"] >= 500:
        d["diamonds"] -= 500
        return "🤝 Союз создан!"
    return "❌ нет алмазов"

# ---- SHOP ----
@app.route("/shop")
def shop():
    return "🛒 Магазин оборудования (V3)"

if __name__ == "__main__":
    app.run()

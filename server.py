from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "xospital_v3"

users = {}

# 2000 пациентов
patients = [{"id": i, "name": f"Пациент {i}", "status": "палата"} for i in range(1, 2001)]

def init_player():
    if "data" not in session:
        session["data"] = {
            "coins": 1000,
            "diamonds": 300,
            "exp": 0,
            "level": 1
        }

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["login"]] = request.form["password"]
        return redirect("/login")
    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["login"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            init_player()
            return redirect("/dashboard")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    init_player()
    d = session["data"]

    return render_template(
        "dashboard.html",
        user=session["user"],
        data=d,
        online=random.randint(5, 50),
        patients=random.sample(patients, 10)
    )

# ---------------- PATIENTS ----------------
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:200])

# ---------------- CALL PATIENT ----------------
@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Пациент {pid} вызван в автопарк"

# ---------------- OPERATING ----------------
@app.route("/operate")
def operate():
    return f"🎲 Кубик: {random.randint(1,6)} → решение операции"

# ---------------- LAB ----------------
@app.route("/lab")
def lab():
    return render_template("lab.html",
        result=random.choice(["кровь","МРТ","рентген","образец"])
    )

# ---------------- ALLIANCE ----------------
@app.route("/alliance")
def alliance():
    init_player()
    d = session["data"]

    if d["diamonds"] >= 500:
        d["diamonds"] -= 500
        return "🤝 Союз создан"
    return "❌ недостаточно алмазов"

# ---------------- SHOP ----------------
@app.route("/shop")
def shop():
    return "🛒 Магазин оборудования"

if __name__ == "__main__":
    app.run()

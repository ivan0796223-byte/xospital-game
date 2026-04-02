from flask import Flask, render_template, request, redirect, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "xospital_v3"

users = {}
messages = []

# 2000 пациентов
patients = [{"id": i, "name": f"Пациент {i}", "status": "палата"} for i in range(1, 2001)]

def init():
    if "data" not in session:
        session["data"] = {
            "coins": 1000,
            "diamonds": 300,
            "exp": 10,
            "level": 1
        }

# ---------- HOME ----------
@app.route("/")
def home():
    return redirect("/login")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        users[request.form["login"]] = request.form["password"]
        return redirect("/login")
    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["login"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            init()
            return redirect("/dashboard")

    return render_template("login.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    init()
    d = session["data"]

    return render_template(
        "dashboard.html",
        user=session["user"],
        data=d,
        online=random.randint(10,100),
        patients=random.sample(patients,10),
        messages=messages[-10:]
    )

# ---------- PATIENTS ----------
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:200])

# ---------- CALL ----------
@app.route("/call/<int:id>")
def call(id):
    return f"🚑 Пациент {id} отправлен"

# ---------- GARAGE ----------
@app.route("/garage")
def garage():
    return render_template("garage.html")

# ---------- OPERATING ----------
@app.route("/operate")
def operate():
    dice = random.randint(1,6)
    return f"🎲 Выпало: {dice} → врач выбран"

# ---------- LAB ----------
@app.route("/lab")
def lab():
    result = random.choice(["анализ крови","рентген","МРТ","образец"])
    return render_template("lab.html", result=result)

# ---------- ALLIANCE ----------
@app.route("/alliance")
def alliance():
    init()
    d = session["data"]

    if d["diamonds"] >= 500:
        d["diamonds"] -= 500
        return "🤝 Союз создан!"
    return "❌ Нужно 500 алмазов"

# ---------- SHOP ----------
@app.route("/shop")
def shop():
    return "🛒 Магазин оборудования"

# ---------- DOCTOR ----------
@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

# ---------- CHAT ----------
@app.route("/chat", methods=["POST"])
def chat():
    now = datetime.now().strftime("%H:%M МСК")
    messages.append(f"{now} {session['user']}: {request.form['msg']}")
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run()

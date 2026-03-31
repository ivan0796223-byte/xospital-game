from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

# 🔐 СЕКРЕТ
app.config["SECRET_KEY"] = "xospital-secret-key"

# 🧠 ВАЖНО: безопасная БД для Render
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 👤 МОДЕЛЬ ИГРОКА
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    coins = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

# 🏥 ПАЦИЕНТЫ
patients_list = [
    "Пациент с переломом",
    "Пациент с простудой",
    "Пациент после аварии",
    "Пациент с болью в животе"
]

# 🏠 ГЛАВНАЯ
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# 📝 РЕГИСТРАЦИЯ
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            return "User exists"

        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

# 🔐 ЛОГИН
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user_id"] = user.id
            return redirect("/")

        return "Wrong login"

    return render_template("login.html")

# 👤 ПАЦИЕНТЫ
@app.route("/patients")
def patients():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("patients.html", patients=patients_list)

# ⚕️ ОПЕРАЦИЯ (ФАРМ)
@app.route("/operate")
def operate():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    user.coins += random.randint(5, 20)
    user.xp += 10

    if user.xp >= 100:
        user.level += 1
        user.xp = 0

    db.session.commit()
    return redirect("/")

# 🚪 ВЫХОД
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# 🚀 ЗАПУСК
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)

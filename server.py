from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key-123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"

db = SQLAlchemy(app)

# ===== МОДЕЛЬ ИГРОКА =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    coins = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

# ===== ПАЦИЕНТЫ =====
patients_list = [
    "Пациент с переломом",
    "Пациент с простудой",
    "Пациент после аварии",
    "Пациент с болью в животе"
]

@app.route("/")
def home():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return render_template("index.html", user=user)
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


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
    return render_template("login.html")


@app.route("/patients")
def patients():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("patients.html", patients=patients_list)


@app.route("/operate")
def operate():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    gain = random.randint(5, 20)
    user.coins += gain
    user.xp += 10

    if user.xp >= 100:
        user.level += 1
        user.xp = 0

    db.session.commit()
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)

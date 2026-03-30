import os
import random
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"

# 🔥 ФИКС БАЗЫ (если нет PostgreSQL → работает SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///game.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== МОДЕЛИ =====
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=5)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(50), default="waiting")

# ===== СОЗДАНИЕ БД =====
with app.app_context():
    db.create_all()

# ===== SAFE PLAYER =====
def get_player():
    username = session.get("user")
    if not username:
        return None
    return Player.query.filter_by(username=username).first()

# ===== РЕГИСТРАЦИЯ =====
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        db.session.add(Player(
            username=request.form["username"],
            password=request.form["password"]
        ))
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

# ===== ЛОГИН =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = Player.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.username
            return redirect("/game")

    return render_template("login.html")

# ===== ИГРА (НЕ ПАДАЕТ) =====
@app.route("/game")
def game():
    player = get_player()

    return render_template(
        "game.html",
        player=player,
        patients=Patient.query.all()
    )

# ===== ПАЦИЕНТЫ =====
@app.route("/add_patient")
def add_patient():
    db.session.add(Patient(name=f"Patient {random.randint(1,999)}"))
    db.session.commit()
    return redirect("/game")

@app.route("/select_patient/<int:id>")
def select_patient(id):
    p = Patient.query.get(id)
    if p:
        p.status = "selected"
        db.session.commit()
    return redirect("/game")

# ===== RUN =====
if __name__ == "__main__":
    app.run()

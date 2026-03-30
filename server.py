import os
import random
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret-key"

# DATABASE SAFE
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///game.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(50), default="waiting")

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    msg = db.Column(db.String(300))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

online_users = set()

with app.app_context():
    db.create_all()

# ================= SAFE PLAYER =================

def get_player():
    username = session.get("user")
    if not username:
        return None
    return Player.query.filter_by(username=username).first()

# ================= AUTH =================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db.session.add(Player(
            username=request.form["username"],
            password=request.form["password"]
        ))
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
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

# ================= GAME SAFE =================

@app.route("/game")
def game():
    player = get_player()

    if session.get("user"):
        online_users.add(session.get("user"))

    return render_template(
        "game.html",
        player=player,
        patients=Patient.query.all(),
        cars=Car.query.all(),
        online=len(online_users)
    )

# ================= CHAT =================

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        db.session.add(Chat(
            user=session.get("user", "guest"),
            msg=request.form["msg"]
        ))
        db.session.commit()

    return render_template("chat.html", messages=Chat.query.all())

# ================= PATIENTS =================

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

# ================= CAR =================

@app.route("/add_car")
def add_car():
    db.session.add(Car(name=random.choice(["🚑 Ambulance", "🚓 Medic Car", "🏥 Van"])))
    db.session.commit()
    return redirect("/game")

@app.route("/call_patient")
def call_patient():
    return f"🚑 Вызов: {random.choice(['Ambulance','Medic Car','Hospital Van'])}"

# ================= OPERATION =================

@app.route("/operation")
def operation():
    roll = random.randint(1, 6)
    return f"🎲 {roll} → {'✔ УСПЕХ' if roll >= 4 else '❌ ПРОВАЛ'}"

# ================= RUN =================

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"

db = SQLAlchemy(app)

# =====================
# МОДЕЛИ
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    text = db.Column(db.Text)

# =====================
# FIX CONTEXT ERROR (ГЛАВНОЕ ИСПРАВЛЕНИЕ)
# =====================
with app.app_context():
    db.create_all()

# =====================
# ONLINE SYSTEM
# =====================
online_users = {}

def add_exp(user, amount):
    user.exp += amount
    if user.exp >= user.level * 100:
        user.level += 1
        user.exp = 0

# =====================
# AUTH
# =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "User exists"

        db.session.add(User(username=u, password=p))
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user_id"] = user.id
            online_users[user.id] = time.time()
            return redirect("/")
        return "Wrong login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
# HOME
# =====================
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# =====================
# REWARD
# =====================
@app.route("/reward")
def reward():
    user = User.query.get(session["user_id"])
    user.coins += 100
    add_exp(user, 20)
    db.session.commit()
    return redirect("/")

# =====================
# CHAT
# =====================
@app.route("/chat", methods=["GET", "POST"])
def chat():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        msg = Message(user=user.username, text=request.form["text"])
        db.session.add(msg)
        db.session.commit()

    return render_template("chat.html", messages=Message.query.all())

# =====================
# PATIENTS (100K VIRTUAL)
# =====================
@app.route("/patients")
def patients():
    patients = []

    for _ in range(12):
        pid = random.randint(1, 100000)
        patients.append({
            "id": pid,
            "name": f"Patient #{pid}",
            "status": random.choice(["stable", "critical", "waiting"])
        })

    return render_template("patients.html", patients=patients)

# =====================
# SELECT PATIENT
# =====================
@app.route("/select/<int:pid>")
def select(pid):
    session["patient"] = pid
    return redirect("/patients")

# =====================
# AMBULANCE / AUTO
# =====================
@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Ambulance sent to patient {pid}"

# =====================
# SURGERY (DICE GAME)
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1, 6)

    if roll <= 2:
        result = "❌ Failure"
    elif roll <= 5:
        result = "⚠ Stable"
    else:
        result = "✅ Success"

    return render_template("surgery.html", roll=roll, result=result)

# =====================
# LAB
# =====================
@app.route("/lab")
def lab():
    return f"🧪 Result: {random.choice(['Virus', 'Healthy', 'Infection', 'Unknown'])}"

# =====================
# EXCHANGE
# =====================
@app.route("/exchange")
def exchange():
    user = User.query.get(session["user_id"])

    if user.coins >= 500:
        user.coins -= 500
        user.diamonds += 1
        db.session.commit()
        return "Exchanged!"

    return "Not enough coins"

# =====================
# ONLINE COUNT
# =====================
@app.route("/online")
def online():
    return jsonify({"online": len(online_users)})

# =====================
# API STATS
# =====================
@app.route("/api/stats")
def stats():
    user = User.query.get(session["user_id"])

    return jsonify({
        "coins": user.coins,
        "diamonds": user.diamonds,
        "exp": user.exp,
        "level": user.level
    })

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

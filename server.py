from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"
db = SQLAlchemy(app)

# =====================
# USER
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

db.create_all()

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
# REGISTER / LOGIN
# =====================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if User.query.filter_by(username=u).first():
            return "exists"
        db.session.add(User(username=u, password=p))
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user_id"] = user.id
            return redirect("/")
        return "error"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
# LEVEL SYSTEM
# =====================
def add_exp(user, amount):
    user.exp += amount
    if user.exp >= user.level * 100:
        user.level += 1
        user.exp = 0

# =====================
# REWARD
# =====================
@app.route("/reward")
def reward():
    u = User.query.get(session["user_id"])
    u.coins += 100
    add_exp(u, 20)
    db.session.commit()
    return redirect("/")

# =====================
# CHAT
# =====================
@app.route("/chat", methods=["GET","POST"])
def chat():
    u = User.query.get(session["user_id"])
    if request.method == "POST":
        db.session.add(Message(user=u.username, text=request.form["text"]))
        db.session.commit()
    return render_template("chat.html", messages=Message.query.all())

# =====================
# PATIENTS (100K VIRTUAL)
# =====================
@app.route("/patients")
def patients():
    page = int(request.args.get("page", 1))
    per_page = 10

    patients = []
    for i in range(per_page):
        pid = random.randint(1, 100000)
        patients.append({
            "id": pid,
            "name": f"Patient #{pid}",
            "status": random.choice(["stable", "critical", "waiting"])
        })

    return render_template("patients.html", patients=patients, page=page)

# =====================
# AMBULANCE / CAR CALL
# =====================
@app.route("/ambulance/<int:pid>")
def ambulance(pid):
    return f"🚑 Patient {pid} sent to hospital"

# =====================
# OPERATING ROOM (DICE GAME)
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1, 6)

    if roll <= 2:
        result = "❌ Failed operation"
    elif roll <= 5:
        result = "⚠️ Stable condition"
    else:
        result = "✅ Success!"

    return render_template("surgery.html", roll=roll, result=result)

# =====================
# LAB
# =====================
@app.route("/lab")
def lab():
    return f"🧪 Analysis result: {random.choice(['Virus', 'Healthy', 'Infection', 'Unknown'])}"

# =====================
# API STATS
# =====================
@app.route("/api/stats")
def stats():
    u = User.query.get(session["user_id"])
    return jsonify({
        "coins": u.coins,
        "diamonds": u.diamonds,
        "exp": u.exp,
        "level": u.level
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

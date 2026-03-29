from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secretkey"
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
# ONLINE SYSTEM
# =====================
online = {}

def add_exp(u, val):
    u.exp += val
    if u.exp >= u.level * 100:
        u.level += 1
        u.exp = 0

# =====================
# AUTH
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
            online[user.id] = time.time()
            return redirect("/")
        return "error"

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

    u = User.query.get(session["user_id"])
    return render_template("index.html", user=u)

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
    patients = []

    for _ in range(12):
        pid = random.randint(1, 100000)
        patients.append({
            "id": pid,
            "name": f"Patient #{pid}",
            "status": random.choice(["stable","critical","waiting"])
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
# AMBULANCE / AUTOPARK
# =====================
@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Ambulance sent to patient {pid}"

# =====================
# SURGERY (DICE SYSTEM)
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1, 6)

    if roll <= 2:
        res = "❌ Failure"
    elif roll <= 5:
        res = "⚠ Stable"
    else:
        res = "✅ Success"

    return render_template("surgery.html", roll=roll, result=res)

# =====================
# LAB
# =====================
@app.route("/lab")
def lab():
    return f"🧪 Diagnosis: {random.choice(['Virus','Healthy','Infection','Unknown'])}"

# =====================
# EXCHANGE
# =====================
@app.route("/exchange")
def exchange():
    u = User.query.get(session["user_id"])

    if u.coins >= 500:
        u.coins -= 500
        u.diamonds += 1
        db.session.commit()
        return "Exchanged!"
    return "Not enough coins"

# =====================
# ONLINE COUNT
# =====================
@app.route("/online")
def online_count():
    return jsonify({"online": len(online)})

# =====================
# API
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
    

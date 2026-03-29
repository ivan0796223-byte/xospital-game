from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================== USER ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

# ================== PATIENT ==================
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    status = db.Column(db.String(50), default="waiting")

with app.app_context():
    db.create_all()

# ================== HOME ==================
@app.route("/")
def home():
    if "user" in session:
        return f"🏥 Hospital Game | Пользователь: {session['user']}"
    return redirect("/login")

# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "User exists"

        user = User(username=u, password=p, coins=100, diamonds=5, xp=0)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return """
    <form method="post">
        <input name="username" placeholder="login">
        <input name="password" type="password" placeholder="password">
        <button>Register</button>
    </form>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user"] = user.username
            return redirect("/")
        return "error login"

    return """
    <form method="post">
        <input name="username">
        <input name="password" type="password">
        <button>Login</button>
    </form>
    """

# ================== PATIENTS ==================
@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    return jsonify([
        {"id": i, "name": f"Patient {i}", "status": "waiting"}
        for i in range(1, 100001)
    ])

# ================== AUTO PARK ==================
@app.route("/ambulance")
def ambulance():
    return jsonify([
        {"id": 1, "car": "🚑 Basic Ambulance"},
        {"id": 2, "car": "🚑 Fast Ambulance"},
    ])

# ================== OPERATION (DICE GAME) ==================
@app.route("/operate")
def operate():
    result = random.randint(1, 6)
    if result >= 4:
        return "Operation SUCCESS 🎉"
    return "Operation FAILED 💀"

# ================== CHAT (SIMPLE MOCK) ==================
messages = []

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = request.json["msg"]
        messages.append(msg)
        return {"ok": True}

    return jsonify(messages)

# ================== REKVIZITY ==================
@app.route("/rekvizity")
def rekvizity():
    return "<h1>Hospital Game Requisites</h1>"

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

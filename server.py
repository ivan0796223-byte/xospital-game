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
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
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
        return f"🏥 Hospital Game | {session['user']}"
    return redirect("/login")

# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "❌ User already exists"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="post">
        <input name="username" placeholder="login"><br>
        <input name="password" type="password" placeholder="password"><br>
        <button>Register</button>
    </form>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user"] = user.username
            return redirect("/")
        return "❌ Wrong login"

    return """
    <h2>Login</h2>
    <form method="post">
        <input name="username"><br>
        <input name="password" type="password"><br>
        <button>Login</button>
    </form>
    """

# ================== PATIENTS (LAZY LOAD) ==================
@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    limit = int(request.args.get("limit", 50))

    return jsonify([
        {"id": i, "name": f"Patient {i}", "status": "waiting"}
        for i in range(1, limit + 1)
    ])

# ================== AMBULANCE ==================
@app.route("/ambulance")
def ambulance():
    return jsonify([
        {"id": 1, "car": "🚑 Basic Ambulance"},
        {"id": 2, "car": "🚑 Fast Ambulance"},
        {"id": 3, "car": "🚑 Elite Rescue"}
    ])

# ================== OPERATION (DICE) ==================
@app.route("/operate")
def operate():
    roll = random.randint(1, 6)

    if roll >= 5:
        return jsonify({"result": "SUCCESS", "roll": roll})
    return jsonify({"result": "FAIL", "roll": roll})

# ================== CHAT (SIMPLE) ==================
messages = []

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = request.json.get("msg", "")
        messages.append(msg)
        return {"ok": True}

    return jsonify(messages)

# ================== REKVIZITY ==================
@app.route("/rekvizity")
def rekvizity():
    return """
    <h1>Hospital Game</h1>
    <p>Working system ✔</p>
    """

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

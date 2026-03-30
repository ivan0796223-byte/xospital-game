from flask import Flask, render_template_string, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================== USERS ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=10)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    last_online = db.Column(db.Integer, default=0)

# ================== PATIENTS ==================
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    disease = db.Column(db.String(120))
    status = db.Column(db.String(50), default="waiting")

with app.app_context():
    db.create_all()

# ================== ONLINE SYSTEM ==================
def update_online(user):
    user.last_online = int(time.time())
    db.session.commit()

def get_online_count():
    now = int(time.time())
    return User.query.filter(User.last_online > now - 60).count()

# ================== HOME ==================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()
    update_online(user)

    return render_template_string("""
    <h1>🏥 Hospital Game</h1>

    <p>👤 {{u.username}}</p>
    <p>💰 {{u.coins}} | 💎 {{u.diamonds}} | ⭐ XP {{u.xp}} | Lv {{u.level}}</p>

    <p>🟢 Online: {{online}}</p>

    <hr>

    <a href="/patients">👨‍⚕ Patients</a><br>
    <a href="/ambulance">🚑 AutoPark</a><br>
    <a href="/operate">🎲 Operation</a><br>
    <a href="/shop">🛒 Shop</a><br>
    <a href="/chat">💬 Chat</a><br>
    """, u=user, online=get_online_count())

# ================== REGISTER ==================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "User exists"

        user = User(username=u, password=p)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return """
    <form method="post">
    <input name="username"><br>
    <input name="password"><br>
    <button>Register</button>
    </form>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user"] = u
            return redirect("/")
        return "Wrong"

    return """
    <form method="post">
    <input name="username"><br>
    <input name="password"><br>
    <button>Login</button>
    </form>
    """

# ================== PATIENT GENERATOR (50K diseases simulated) ==================
DISEASES = [
    "Flu","Covid","Fracture","Heart Attack","Migraine","Infection","Burn","Asthma"
]

@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    # НЕ создаём 50k реально — генерируем виртуально
    data = []
    for i in range(1, 20):
        data.append({
            "id": i,
            "name": f"Patient {i}",
            "disease": random.choice(DISEASES),
            "status": "waiting"
        })

    return jsonify(data)

# ================== AMBULANCE ==================
@app.route("/ambulance")
def ambulance():
    cars = [
        {"id":1,"car":"🚑 Basic"},
        {"id":2,"car":"🚑 Fast"},
        {"id":3,"car":"🚑 ICU Truck"}
    ]
    return jsonify(cars)

# ================== OPERATION (DICE GAME) ==================
@app.route("/operate")
def operate():
    roll = random.randint(1,6)

    if roll >= 5:
        return {"result":"SUCCESS","roll":roll,"xp":10}
    return {"result":"FAIL","roll":roll,"xp":2}

# ================== SHOP ==================
@app.route("/shop")
def shop():
    return """
    <h2>🛒 Shop</h2>
    <p>🩺 Equipment</p>
    <p>🚑 Cars upgrade</p>
    <p>💊 Medicines</p>
    """

# ================== CHAT (simple mock) ==================
messages = []

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        messages.append(request.json["msg"])
        return {"ok":True}

    return jsonify(messages)

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

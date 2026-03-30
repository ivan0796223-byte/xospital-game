import os
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
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
alliances = []

with app.app_context():
    db.create_all()

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

# ================= GAME =================

@app.route("/game")
def game():
    player = Player.query.filter_by(username=session.get("user")).first()

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
            user=session.get("user"),
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
    p.status = "selected"
    db.session.commit()
    return redirect("/game")

# ================= CAR / CALL =================

@app.route("/add_car")
def add_car():
    db.session.add(Car(name=random.choice(["🚑 Ambulance", "🚓 Medic Car", "🏥 Van"])))
    db.session.commit()
    return redirect("/game")

@app.route("/call_patient")
def call_patient():
    return f"🚑 Вызов: {random.choice(['Ambulance', 'Medic Car', 'Hospital Van'])}"

# ================= OPERATION (DICE) =================

@app.route("/operation")
def operation():
    roll = random.randint(1, 6)
    return f"🎲 Кубик: {roll} → {'✔ УСПЕХ' if roll >= 4 else '❌ ПРОВАЛ'}"

# ================= TIME (MSK) =================

@app.route("/time")
def time_msk():
    return f"🕒 МСК: {datetime.utcnow()} (UTC approx)"

# ================= EVENTS =================

@app.route("/patients_event")
def patients_event():
    return f"🚨 Событие: {random.randint(1,20)} пациентов появилось"

@app.route("/patients_50000")
def patients_50000():
    return "📊 Пациенты: 50 000 (виртуально)"

# ================= ALLIANCES =================

@app.route("/create_alliance", methods=["POST"])
def create_alliance():
    name = request.form.get("name")
    player = Player.query.filter_by(username=session.get("user")).first()

    if player and player.diamonds >= 500:
        player.diamonds -= 500
        alliances.append(name)
        db.session.commit()
        return f"🤝 Союз создан: {name}"

    return "❌ Не хватает алмазов"

@app.route("/alliances")
def show_alliances():
    return {"alliances": alliances}

# ================= SEARCH =================

@app.route("/search_player/<name>")
def search_player(name):
    u = Player.query.filter_by(username=name).first()
    return f"👤 {u.username} LVL {u.level}" if u else "❌ не найден"

@app.route("/search_alliance/<name>")
def search_alliance(name):
    return f"🤝 найден: {name}" if name in alliances else "❌ не найден"

# ================= SHOP / BANK =================

@app.route("/shop")
def shop():
    return "🏪 Магазин: скальпель / авто / аптечки"

@app.route("/bank")
def bank():
    return "🏦 Банк: обмен валют (в разработке)"

@app.route("/doctor_room")
def doctor_room():
    player = Player.query.filter_by(username=session.get("user")).first()
    return f"🏥 Кабинет: {player.username} 💰{player.coins} 💎{player.diamonds}"

# ================= RUN =================

if __name__ == "__main__":
    app.run()

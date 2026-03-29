from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)

# ================== CONFIG ==================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

db = SQLAlchemy(app)

# ================== MODELS ==================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    last_online = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    text = db.Column(db.String(500))
    time = db.Column(db.String(20))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    item = db.Column(db.String(100))

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100))
    patient_id = db.Column(db.Integer)
    dice = db.Column(db.Integer)
    result = db.Column(db.String(50))

# ================== INIT DB SAFE ==================

def init_db():
    with app.app_context():
        db.create_all()

init_db()

# ================== HELPERS ==================

def progress(user):
    need = user.level * 100
    return int((user.exp / need) * 100)

def get_online():
    return User.query.filter(User.last_online != None).count()

def virtual_patient(pid):
    return {
        "id": pid,
        "name": f"Patient #{pid}",
        "room": f"Room {pid % 50 + 1}",
        "status": "waiting"
    }

# ================== ROUTES ==================

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()
    if not user:
        return redirect("/login")

    user.last_online = datetime.utcnow()
    db.session.commit()

    return render_template("index.html",
                           user=user,
                           progress=progress(user),
                           online=get_online())

# ================== AUTH ==================

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
            session["user"] = user.username
            return redirect("/")
        return "Wrong login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================== PATIENTS (100K VIRTUAL) ==================

@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    data = [virtual_patient(i) for i in range(1, 51)]
    return render_template("patients.html", patients=data)


@app.route("/select_patient/<int:pid>")
def select_patient(pid):
    session["patient"] = pid
    return redirect("/operating")

# ================== OPERATING + DICE ==================

@app.route("/operating")
def operating():
    if "user" not in session:
        return redirect("/login")

    pid = session.get("patient", 1)
    patient = virtual_patient(pid)

    return render_template("operating.html", patient=patient)


@app.route("/dice")
def dice():
    roll = random.randint(1, 6)

    result = "FAIL"
    if roll >= 4:
        result = "SUCCESS"

    db.session.add(Operation(
        doctor=session.get("user"),
        patient_id=session.get("patient", 0),
        dice=roll,
        result=result
    ))
    db.session.commit()

    return jsonify({"roll": roll, "result": result})

# ================== CHAT ==================

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        db.session.add(Message(
            user=session.get("user"),
            text=request.form["text"],
            time=datetime.now().strftime("%H:%M")
        ))
        db.session.commit()
        return redirect("/chat")

    return render_template("chat.html", messages=Message.query.all())

# ================== SHOP ==================

@app.route("/shop")
def shop():
    items = ["Medkit", "Scanner", "Upgrade", "Armor"]
    return render_template("shop.html", items=items)

@app.route("/buy/<item>")
def buy(item):
    user = User.query.filter_by(username=session["user"]).first()
    user.coins += 0  # можно заменить логикой
    db.session.add(Inventory(user=user.username, item=item))
    db.session.commit()
    return redirect("/shop")

# ================== GARAGE ==================

@app.route("/garage")
def garage():
    cars = Vehicle.query.filter_by(user=session["user"]).all()
    return render_template("garage.html", cars=cars)

@app.route("/add_car/<name>")
def add_car(name):
    db.session.add(Vehicle(user=session["user"], name=name))
    db.session.commit()
    return redirect("/garage")

# ================== ONLINE API ==================

@app.route("/api/online")
def online():
    return jsonify({"online": get_online()})

# ================== RUN ==================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret"

db = SQLAlchemy(app)

# ===================== MODELS =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(50), default="waiting")  # waiting, in_room, surgery
    assigned_to = db.Column(db.String(100))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    text = db.Column(db.String(500))
    time = db.Column(db.String(50))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    item = db.Column(db.String(100))

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    name = db.Column(db.String(100))
    level = db.Column(db.Integer, default=1)

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100))
    patient_id = db.Column(db.Integer)
    result = db.Column(db.String(100))
    dice = db.Column(db.Integer)

# ===================== INIT DB =====================

with app.app_context():
    db.create_all()

# ===================== HELPERS =====================

def level_progress(user):
    need = user.level * 100
    return int((user.exp / need) * 100)

def get_online_users():
    return User.query.filter(User.last_seen != None).all()

# ===================== ROUTES =====================

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()
    user.last_seen = datetime.utcnow()
    db.session.commit()

    return render_template("index.html", user=user, progress=level_progress(user))


# ===================== AUTH =====================

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

# ===================== PATIENT SYSTEM (100K VIRTUAL) =====================

@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    # показываем только часть (реально не храним 100k)
    sample = [
        {"id": i, "name": f"Patient #{i}", "status": "waiting"}
        for i in range(1, 51)
    ]

    return render_template("patients.html", patients=sample)


@app.route("/select_patient/<int:pid>")
def select_patient(pid):
    session["patient"] = pid
    return redirect("/operating")


# ===================== OPERATING ROOM + DICE =====================

@app.route("/operating")
def operating():
    if "user" not in session:
        return redirect("/login")

    patient = session.get("patient", None)
    return render_template("operating.html", patient=patient)


@app.route("/dice")
def dice():
    roll = random.randint(1, 6)

    result = "FAIL"
    if roll >= 4:
        result = "SUCCESS"

    op = Operation(
        doctor=session.get("user"),
        patient_id=session.get("patient", 0),
        result=result,
        dice=roll
    )
    db.session.add(op)
    db.session.commit()

    return jsonify({"roll": roll, "result": result})


# ===================== CHAT =====================

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = Message(
            user=session.get("user"),
            text=request.form["text"],
            time=str(datetime.now().strftime("%H:%M"))
        )
        db.session.add(msg)
        db.session.commit()

        return redirect("/chat")

    return render_template("chat.html", messages=Message.query.all())


# ===================== SHOP =====================

@app.route("/shop")
def shop():
    items = ["Medkit", "Scanner", "Upgrade Tool", "Car Engine"]
    return render_template("shop.html", items=items)


@app.route("/buy/<item>")
def buy(item):
    user = User.query.filter_by(username=session["user"]).first()
    user.coins -= 10

    db.session.add(Inventory(user=user.username, item=item))
    db.session.commit()

    return redirect("/shop")


# ===================== VEHICLES =====================

@app.route("/garage")
def garage():
    cars = Vehicle.query.filter_by(user=session["user"]).all()
    return render_template("garage.html", cars=cars)


@app.route("/add_car/<name>")
def add_car(name):
    db.session.add(Vehicle(user=session["user"], name=name))
    db.session.commit()
    return redirect("/garage")


# ===================== API =====================

@app.route("/api/online")
def online():
    users = User.query.all()
    return jsonify(len(users))


# ===================== RUN =====================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

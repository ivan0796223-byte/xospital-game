from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"

db = SQLAlchemy(app)

# ===== USER =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))
    coins = db.Column(db.Integer, default=1000)
    diamonds = db.Column(db.Integer, default=10)
    exp = db.Column(db.Integer, default=0)

# ===== CHAT =====
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    user = db.Column(db.String(50))

# ===== 5000 PATIENTS =====
patients = [f"Пациент #{i}" for i in range(1, 5001)]

# ===== HOME =====
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    online = User.query.count()
    msgs = Message.query.order_by(Message.id.desc()).limit(20)

    now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

    level = user.exp // 100
    progress = user.exp % 100

    return render_template("game.html",
                           user=user,
                           online=online,
                           msgs=msgs,
                           now=now,
                           level=level,
                           progress=progress)

# ===== REGISTER =====
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if User.query.filter_by(login=login).first():
            return "exists"

        u = User(login=login,
                 password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# ===== LOGIN =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect("/")

        return "error"

    return render_template("login.html")

# ===== CHAT SEND =====
@app.route("/send", methods=["POST"])
def send():
    user = User.query.get(session["user_id"])
    text = request.form["text"]

    db.session.add(Message(text=text, user=user.login))
    db.session.commit()
    return redirect("/")

# ===== PATIENTS =====
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:200])

# ===== CALL PATIENT =====
@app.route("/call")
def call():
    return f"🚑 Вызов: {random.choice(patients)}"

# ===== OPERATION DICE =====
@app.route("/operation")
def operation():
    return f"🎲 Кубик: {random.randint(1,6)}"

# ===== LAB =====
@app.route("/lab")
def lab():
    return f"🧪 Результат: {random.choice(['Чисто','Инфекция','Срочный случай'])}"

# ===== EXCHANGE =====
@app.route("/exchange")
def exchange():
    u = User.query.get(session["user_id"])
    u.coins -= 100
    u.diamonds += 1
    db.session.commit()
    return redirect("/")

# ===== ALLIANCE =====
@app.route("/alliance")
def alliance():
    return "👥 Союзы + ЗАГС (скоро)"

# ===== DB =====
with app.app_context():
    db.create_all()

app.run()

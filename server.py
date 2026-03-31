from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"

db = SQLAlchemy(app)

# ===== МОДЕЛИ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))
    coins = db.Column(db.Integer, default=1000)
    diamonds = db.Column(db.Integer, default=50)
    exp = db.Column(db.Integer, default=0)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    user = db.Column(db.String(50))

patients = [f"Пациент {i}" for i in range(1, 5001)]

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    online = User.query.count()
    msgs = Message.query.order_by(Message.id.desc()).limit(20)

    time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    level = user.exp // 100
    progress = user.exp % 100

    return render_template("game.html",
                           user=user,
                           online=online,
                           msgs=msgs,
                           time=time,
                           level=level,
                           progress=progress)

# ===== РЕГИСТРАЦИЯ =====
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if User.query.filter_by(login=login).first():
            return "Пользователь уже есть"

        user = User(login=login,
                    password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# ===== ВХОД =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect("/")

    return render_template("login.html")

# ===== ЧАТ =====
@app.route("/send", methods=["POST"])
def send():
    user = User.query.get(session["user_id"])
    text = request.form.get("text")

    db.session.add(Message(text=text, user=user.login))
    db.session.commit()
    return redirect("/")

# ===== ПАЦИЕНТЫ =====
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:200])

# ===== АВТОПАРК =====
@app.route("/garage")
def garage():
    call = random.choice(patients)
    return f"🚑 Вызов: {call}"

# ===== ОПЕРАЦИОННАЯ =====
@app.route("/operate")
def operate():
    dice = random.randint(1, 6)
    return f"🎲 Выпало: {dice}"

# ===== ЛАБОРАТОРИЯ =====
@app.route("/lab")
def lab():
    result = random.choice([
        "Анализ чистый",
        "Инфекция обнаружена",
        "Редкое заболевание"
    ])
    return f"🧪 {result}"

# ===== ОБМЕННИК =====
@app.route("/exchange")
def exchange():
    user = User.query.get(session["user_id"])
    if user.coins >= 100:
        user.coins -= 100
        user.diamonds += 1
        db.session.commit()
    return redirect("/")

# ===== СОЮЗ =====
@app.route("/alliance")
def alliance():
    return "👥 Союз / ЗАГС (скоро полный функционал)"

# ===== КАБИНЕТ ДОКТОРА =====
@app.route("/doctor")
def doctor():
    return "👨‍⚕️ Кабинет доктора"

# ===== БАЗА =====
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
                           

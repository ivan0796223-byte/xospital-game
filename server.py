from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-key-123"

db = SQLAlchemy(app)

# =====================
# МОДЕЛИ
# =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    text = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow)

# =====================
# СОЗДАНИЕ БД
# =====================

with app.app_context():
    db.create_all()

# =====================
# ГЛАВНАЯ
# =====================

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# =====================
# РЕГИСТРАЦИЯ
# =====================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Пользователь уже существует"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# =====================
# ВХОД
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect(url_for("index"))

        return "Неверный логин или пароль"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =====================
# ПАЦИЕНТЫ (заглушка)
# =====================

@app.route("/patients")
def patients():
    if "user_id" not in session:
        return redirect(url_for("login"))

    users = User.query.all()
    return render_template("patients.html", users=users)

# =====================
# ЧАТ
# =====================

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        text = request.form["text"]

        msg = Message(username=user.username, text=text)
        db.session.add(msg)
        db.session.commit()

    messages = Message.query.order_by(Message.id.asc()).all()
    return render_template("chat.html", messages=messages, user=user)

# =====================
# НАГРАДА (тест кнопок)
# =====================

@app.route("/reward")
def reward():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    user.coins += 100
    user.exp += 20

    # уровень
    if user.exp >= user.level * 100:
        user.level += 1
        user.exp = 0

    db.session.commit()

    return redirect(url_for("index"))

# =====================
# API (для кнопок без перезагрузки)
# =====================

@app.route("/api/stats")
def api_stats():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"})

    user = User.query.get(session["user_id"])

    return jsonify({

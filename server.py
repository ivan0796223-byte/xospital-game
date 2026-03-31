from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# ===== МОДЕЛЬ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=10)
    exp = db.Column(db.Integer, default=0)

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# ===== РЕГИСТРАЦИЯ =====
@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            login = request.form.get("login")
            password = request.form.get("password")

            if not login or not password:
                return "Заполните все поля"

            if User.query.filter_by(login=login).first():
                return "Пользователь уже существует"

            password_hash = generate_password_hash(password)
            user = User(login=login, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return redirect("/login")
    except Exception as e:
        app.logger.error(f"Ошибка при регистрации: {e}")
        return "Произошла ошибка. Попробуйте позже."

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
        else:
            return "Неверный логин или пароль"

    return render_template("login.html")

# ===== ПАЦИЕНТЫ =====
@app.route("/patients")
def patients():
    if "user_id" not in session:
        return redirect("/login")

    data = ["Пациент 1", "Пациент 2", "Пациент 3"]
    return render_template("patients.html", patients=data)

# ===== ВЫХОД =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== СОЗДАНИЕ БД =====
with app.app_context():
    db.create_all()

# ===== ЗАПУСК =====
if __name__ == "__main__":
    app.run(debug=True)

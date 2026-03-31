from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== МОДЕЛЬ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    return "Ты вошёл в игру 🎮"

# ===== РЕГИСТРАЦИЯ =====
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            login = request.form.get("login")
            password = request.form.get("password")

            print("LOGIN:", login)

            if not login or not password:
                return "❌ Заполни все поля"

            if User.query.filter_by(login=login).first():
                return "❌ Такой пользователь уже есть"

            password_hash = generate_password_hash(password)

            user = User(login=login, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return redirect("/login")

        except Exception as e:
            db.session.rollback()
            return f"❌ Ошибка: {e}"

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
            return "❌ Неверный логин или пароль"

    return render_template("login.html")

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

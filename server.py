from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== МОДЕЛЬ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
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
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if User.query.filter_by(login=login).first():
            return "Пользователь уже есть"

        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# ===== ВХОД =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = User.query.filter_by(login=login, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/")
        else:
            return "Ошибка входа"

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

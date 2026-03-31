from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== МОДЕЛЬ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# ===== ГЛАВНАЯ =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== РЕГИСТРАЦИЯ =====
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Пустые поля"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# ===== ЛОГИН =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect(url_for("patients"))
        else:
            return "Неверный логин"

    return render_template("login.html")

# ===== ПАЦИЕНТЫ =====
@app.route("/patients")
def patients():
    if "user_id" not in session:
        return redirect(url_for("login"))

    patients_list = [
        "Пациент №1",
        "Пациент №2",
        "Пациент №3",
        "Пациент №4"
    ]

    return render_template("patients.html", patients=patients_list)

# ===== ВЫХОД =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== ТЕСТ (ПРОВЕРКА СЕРВЕРА) =====
@app.route("/test")
def test():
    return "OK сервер работает"

# ===== СОЗДАНИЕ БД =====
with app.app_context():
    db.create_all()

# ===== ЗАПУСК =====
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ================== МОДЕЛЬ ИГРОКА ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

# ================== 100k ПАЦИЕНТОВ ==================
patients = [f"Пациент #{i}" for i in range(1, 100001)]

# ================== ОНЛАЙН ==================
online_users = set()

# ================== РЕГИСТРАЦИЯ ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User(username=u, password=p)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

# ================== ЛОГИН ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user"] = user.username
            online_users.add(user.username)
            return redirect("/game")

    return render_template("login.html")

# ================== ИГРА ==================
@app.route("/game")
def game():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()
    return render_template("game.html", user=user, online=len(online_users))

# ================== ПАЦИЕНТЫ ==================
@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=random.sample(patients, 20))

# ================== ОПЕРАЦИЯ (КУБИКИ) ==================
@app.route("/operation")
def operation():
    roll = random.randint(1, 6)
    return f"🎲 Выпало: {roll}"

# ================== ЧАТ ==================
@socketio.on("message")
def handle(msg):
    send(msg, broadcast=True)

# ================== ЗАПУСК ==================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(app, host="0.0.0.0", port=5000)

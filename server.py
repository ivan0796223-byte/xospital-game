from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import traceback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"

db = SQLAlchemy(app)

# =====================
# MODELS
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=5)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    text = db.Column(db.Text)

# =====================
# INIT DB
# =====================
with app.app_context():
    db.create_all()

online_users = set()

# =====================
# HOME
# =====================
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                return "Пустые поля"

            if User.query.filter_by(username=username).first():
                return "Уже существует"

            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect("/login")

        except Exception:
            return "<pre>" + traceback.format_exc() + "</pre>"

    return render_template("register.html")

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            online_users.add(user.id)
            return redirect("/")

        return "Неверный логин"

    return render_template("login.html")

# =====================
# LOGOUT
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
# CHAT
# =====================
@app.route("/chat", methods=["GET", "POST"])
def chat():
    user = User.query.get(session.get("user_id"))

    if request.method == "POST":
        text = request.form.get("text")
        if text:
            msg = Message(user=user.username, text=text)
            db.session.add(msg)
            db.session.commit()

    messages = Message.query.all()
    return render_template("chat.html", messages=messages)

# =====================
# PATIENTS (100K SIMULATION)
# =====================
@app.route("/patients")
def patients():
    data = []

    for _ in range(10):
        pid = random.randint(1, 100000)
        data.append({
            "id": pid,
            "name": f"Patient {pid}",
            "status": random.choice(["stable", "critical", "waiting"])
        })

    return render_template("patients.html", patients=data)

# =====================
# CALL PATIENT
# =====================
@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Вызов пациента {pid}"

# =====================
# SURGERY DICE
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1, 6)

    if roll <= 2:
        result = "❌ Провал"
    elif roll <= 5:
        result = "⚠ Стабильно"
    else:
        result = "✅ Успех"

    return render_template("surgery.html", roll=roll, result=result)

# =====================
# LAB
# =====================
@app.route("/lab")
def lab():
    return jsonify({
        "result": random.choice(["Virus", "Healthy", "Infection", "Unknown"])
    })

# =====================
# EXCHANGE
# =====================
@app.route("/exchange")
def exchange():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.coins >= 500:
        user.coins -= 500
        user.diamonds += 1
        db.session.commit()
        return "Обмен выполнен"

    return "Недостаточно монет"

# =====================
# ONLINE COUNT
# =====================
@app.route("/online")
def online():
    return jsonify({"online": len(online_users)})

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

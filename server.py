from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random, time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret123"

db = SQLAlchemy(app)

# =====================
# MODELS
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
    user = db.Column(db.String(80))
    text = db.Column(db.Text)

# ✅ FIX CONTEXT
with app.app_context():
    db.create_all()

online = {}

# =====================
# HELPERS
# =====================
def add_exp(u, val):
    u.exp += val
    if u.exp >= u.level * 100:
        u.level += 1
        u.exp = 0

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        try:
            u = request.form.get("username")
            p = request.form.get("password")

            if not u or not p:
                return "Введите логин и пароль"

            if User.query.filter_by(username=u).first():
                return "Пользователь уже существует"

            new_user = User(username=u, password=p)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

        except Exception as e:
            return f"Ошибка регистрации: {str(e)}"

    return render_template("register.html")

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        try:
            u = request.form.get("username")
            p = request.form.get("password")

            if not u or not p:
                return "Введите данные"

            user = User.query.filter_by(username=u, password=p).first()

            if user:
                session["user_id"] = user.id
                online[user.id] = time.time()
                return redirect("/")

            return "Неверный логин"

        except Exception as e:
            return f"Ошибка входа: {str(e)}"

    return render_template("login.html")

# =====================
# LOGOUT
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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
# REWARD
# =====================
@app.route("/reward")
def reward():
    u = User.query.get(session["user_id"])
    u.coins += 100
    add_exp(u, 20)
    db.session.commit()
    return redirect("/")

# =====================
# CHAT
# =====================
@app.route("/chat", methods=["GET","POST"])
def chat():
    u = User.query.get(session["user_id"])

    if request.method == "POST":
        text = request.form.get("text")
        if text:
            db.session.add(Message(user=u.username, text=text))
            db.session.commit()

    return render_template("chat.html", messages=Message.query.all())

# =====================
# PATIENTS (100K)
# =====================
@app.route("/patients")
def patients():
    patients = []
    for _ in range(10):
        pid = random.randint(1, 100000)
        patients.append({
            "id": pid,
            "name": f"Patient {pid}",
            "status": random.choice(["stable","critical","waiting"])
        })
    return render_template("patients.html", patients=patients)

@app.route("/select/<int:pid>")
def select(pid):
    session["patient"] = pid
    return redirect("/patients")

@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Вызов пациента {pid}"

# =====================
# SURGERY (DICE)
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1,6)

    if roll <= 2:
        result = "❌ Неудача"
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
    return f"🧪 {random.choice(['Virus','Healthy','Infection'])}"

# =====================
# EXCHANGE
# =====================
@app.route("/exchange")
def exchange():
    u = User.query.get(session["user_id"])

    if u.coins >= 500:
        u.coins -= 500
        u.diamonds += 1
        db.session.commit()
        return "Обмен выполнен"

    return "Недостаточно монет"

# =====================
# ONLINE
# =====================
@app.route("/online")
def online_count():
    return jsonify({"online": len(online)})

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

# ================== DB ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    text = db.Column(db.String(200))
    time = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# ================== PLAYER DATA ==================
player_data = {
    "coins": 100,
    "diamonds": 5,
    "xp": 0,
    "level": 1
}

# ================== STYLE ==================
STYLE = """
<style>
body{background:#05070c;color:white;font-family:Arial}
.card{background:#0f1722;border:1px solid red;margin:10px;padding:12px;border-radius:12px}
h1,h2{color:#ff2b2b}
button{background:#ff2b2b;color:white;border:none;padding:8px;border-radius:8px}
input{padding:6px;margin:5px}
.icon{width:40px;height:40px;border-radius:50%;background:#1f2a3a;display:inline-block;text-align:center;line-height:40px}
.progress{background:#222;height:10px;border-radius:10px}
.bar{background:#ff2b2b;height:10px;border-radius:10px;width:50%}
.cross{color:red}
</style>
"""

# ================== HOME ==================
@app.route("/")
def home():
    return redirect("/login")

# ================== REGISTER ==================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "exists"

        db.session.add(User(username=u,password=p))
        db.session.commit()
        return redirect("/login")

    return STYLE + """
    <div class='card'>
        <h2>Регистрация ✚</h2>
        <form method='post'>
            <input name='username'><br>
            <input name='password'><br>
            <button>Создать</button>
        </form>
    </div>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u,password=p).first()
        if user:
            session["user"] = u
            return redirect("/panel")

    return STYLE + """
    <div class='card'>
        <h2>Вход ✚</h2>
        <form method='post'>
            <input name='username'><br>
            <input name='password'><br>
            <button>Войти</button>
        </form>
    </div>
    """

# ================== PANEL ==================
@app.route("/panel")
def panel():
    if "user" not in session:
        return redirect("/login")

    return STYLE + f"""
    <div class='card'>
        <h1>🏥 Hospital Game</h1>
        Игрок: {session['user']}

        <br><br>
        <a href='/chat'><button>Чат</button></a>
        <a href='/patients'><button>Пациенты</button></a>
        <a href='/ambulance'><button>Автопарк</button></a>
        <a href='/operation'><button>Операция</button></a>
        <a href='/wards'><button>Палаты</button></a>
        <a href='/online'><button>Онлайн</button></a>
        <a href='/profile'><button>Профиль</button></a>
    </div>
    """

# ================== CHAT ==================
@app.route("/chat", methods=["GET","POST"])
def chat():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        db.session.add(Message(
            user=session["user"],
            text=request.form["text"],
            time=str(datetime.now().strftime("%H:%M"))
        ))
        db.session.commit()
        return redirect("/chat")

    msgs = Message.query.all()

    html = STYLE + "<div class='card'><h2>💬 Чат</h2>"

    for m in msgs[-20:]:
        html += f"<div class='card'>{m.user}: {m.text}</div>"

    html += """
    <form method='post'>
        <input name='text'>
        <button>Send</button>
    </form>
    </div>
    """
    return html

# ================== PATIENTS ==================
@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/login")

    html = STYLE + "<div class='card'><h2>👤 Пациенты</h2>"

    for i in range(1, 10):
        html += f"""
        <div class='card'>
            <div class='icon'>🧑</div>
            Пациент {i}<br>
            Болезнь: неизвестна<br>
            <button>Выбрать</button>
        </div>
        """

    return html + "</div>"

# ================== AMBULANCE ==================
@app.route("/ambulance")
def ambulance():
    if "user" not in session:
        return redirect("/login")

    return STYLE + """
    <div class='card'>
        <h2>🚑 Автопарк</h2>

        <div class='icon'>🚑</div>
        Скорая №1 <a href='/call/1'><button>Вызов</button></a><br><br>

        <div class='icon'>🚑</div>
        Скорая №2 <a href='/call/2'><button>Вызов</button></a>
    </div>
    """

@app.route("/call/<id>")
def call(id):
    return redirect("/ambulance")

# ================== OPERATION ==================
@app.route("/operation")
def operation():
    if "user" not in session:
        return redirect("/login")

    roll = random.randint(1,6)
    result = "SUCCESS" if roll >= 4 else "FAIL"

    player_data["xp"] += 10

    return STYLE + f"""
    <div class='card'>
        <h2>🎲 Операция</h2>
        Кубик: {roll}<br>
        Результат: {result}
        <br><br>
        <a href='/operation'><button>Кинуть ещё</button></a>
    </div>
    """

# ================== PROFILE ==================
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    xp = player_data["xp"]
    lvl = player_data["level"]

    return STYLE + f"""
    <div class='card'>
        <h2>👤 Профиль</h2>

        💰 Монеты: {player_data['coins']}<br>
        💎 Алмазы: {player_data['diamonds']}<br>
        ⭐ XP: {xp}<br>
        🆙 Level: {lvl}

        <div class='progress'>
            <div class='bar' style='width:{xp%100}%'></div>
        </div>
    </div>
    """

# ================== WARDS ==================
@app.route("/wards")
def wards():
    if "user" not in session:
        return redirect("/login")

    html = STYLE + "<div class='card'><h2>🏥 Палаты</h2>"

    for i in range(1,6):
        html += f"""
        <div class='card'>
            🛏 Палата {i}<br>
            Пациент: 🧑 {i*2}
        </div>
        """

    return html + "</div>"

# ================== ONLINE ==================
@app.route("/online")
def online():
    return STYLE + f"""
    <div class='card'>
        <h2>🟢 Онлайн</h2>
        Игроков: {User.query.count()}
    </div>
    """

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

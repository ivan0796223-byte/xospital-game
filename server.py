from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================== ONLINE ==================
online_users = set()
messages = []

# ================== USER ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

with app.app_context():
    db.create_all()

# ================== HOME ==================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()
    online = len(online_users)

    xp_bar = user.xp % 100

    return f"""
    <style>
    body{{background:#05070c;color:white;font-family:Arial}}
    .card{{background:#0f1722;border:1px solid red;padding:15px;margin:10px;border-radius:12px}}
    .box{{display:inline-block;background:#111;border:1px solid red;padding:10px;margin:5px;border-radius:10px}}
    .bar{{background:#222;height:10px;border-radius:5px}}
    .fill{{background:red;height:10px;width:{xp_bar}%;border-radius:5px}}
    button{{background:red;color:white;border:none;padding:8px;margin:5px;border-radius:8px}}
    a{{color:red}}
    </style>

    <div class="card">
        <h2>🏥 Hospital Game PRO</h2>

        <p>👤 {user.username}</p>
        <p>🟢 Онлайн: {online}</p>

        <div class="box">💰 {user.coins}</div>
        <div class="box">💎 {user.diamonds}</div>
        <div class="box">⭐ LVL {user.level}</div>

        <p>XP</p>
        <div class="bar"><div class="fill"></div></div>

        <br>

        <a href="/chat"><button>💬 Чат</button></a>
        <a href="/patients"><button>🧑‍⚕ Пациенты</button></a>
        <a href="/garage"><button>🚑 Автопарк</button></a>
        <a href="/operating"><button>🏥 Операционная</button></a>

        <br><br>
        <a href="/logout">🚪 Выйти</a>
    </div>
    """

# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "❌ Уже есть"

        db.session.add(User(username=username, password=password))
        db.session.commit()

        return redirect("/login")

    return """
    <style>
    body{background:#05070c;color:white;font-family:Arial;text-align:center}
    .card{background:#0f1722;border:1px solid red;padding:20px;margin:50px auto;width:300px;border-radius:12px}
    input{width:90%;padding:8px;margin:5px}
    button{background:red;color:white;border:none;padding:10px;width:95%}
    a{color:red}
    </style>

    <div class="card">
        <h2>🆕 Регистрация</h2>
        <form method="post">
            <input name="username"><br>
            <input name="password"><br>
            <button>Создать</button>
        </form>
        <a href="/login">Вход</a>
    </div>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if not user:
            return "❌ ошибка"

        session["user"] = username
        online_users.add(username)

        return redirect("/")

    return """
    <style>
    body{background:#05070c;color:white;font-family:Arial;text-align:center}
    .card{background:#0f1722;border:1px solid red;padding:20px;margin:50px auto;width:300px;border-radius:12px}
    input{width:90%;padding:8px;margin:5px}
    button{background:red;color:white;border:none;padding:10px;width:95%}
    a{color:red}
    </style>

    <div class="card">
        <h2>🔐 Вход</h2>
        <form method="post">
            <input name="username"><br>
            <input name="password"><br>
            <button>Войти</button>
        </form>
        <a href="/register">Регистрация</a>
    </div>
    """

# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    user = session.get("user")
    if user in online_users:
        online_users.remove(user)

    session.pop("user", None)
    return redirect("/login")

# ================== CHAT ==================
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        messages.append(session["user"] + ": " + request.form["msg"])

    return "<br>".join(messages[-20:]) + """
    <form method="post">
        <input name="msg">
        <button>send</button>
    </form>
    """

# ================== PATIENTS ==================
@app.route("/patients")
def patients():
    return "<h2>Пациенты</h2>"

# ================== GARAGE ==================
@app.route("/garage")
def garage():
    return "<h2>Автопарк</h2> 🚑 🚓 🚒"

# ================== OPERATING ==================
@app.route("/operating")
def operating():
    roll = random.randint(1, 6)
    return f"<h2>Операционная</h2><br>🎲 {roll}"

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

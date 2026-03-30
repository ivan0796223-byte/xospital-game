from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
db = SQLAlchemy(app)

# ================= ONLINE =================
online_users = set()
messages = []

# ================= PATIENTS (50k) =================
patients = [{"id": i, "name": f"Patient #{i}", "hp": random.randint(50, 100)} for i in range(50000)]

# ================= CARS =================
cars = {
    "ambulance": 1000,
    "helicopter": 5000,
    "supercar": 2000
}

user_cars = {}

# ================= ALLIANCES =================
alliances = {}

# ================= USER =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=10)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    alliance = db.Column(db.String(80), default="")

with app.app_context():
    db.create_all()

# ================= HOME =================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    xp_bar = user.xp % 100

    return f"""
    <style>
    body{{background:#05070c;color:white;font-family:Arial}}
    .card{{background:#0f1722;border:2px solid red;padding:15px;margin:10px;border-radius:12px}}
    .box{{display:inline-block;background:#111;border:1px solid red;padding:8px;margin:5px;border-radius:50px}}
    .bar{{background:#222;height:10px;border-radius:10px}}
    .fill{{background:red;height:10px;width:{xp_bar}%;border-radius:10px}}
    button{{background:red;color:white;border:none;padding:8px;margin:5px;border-radius:10px}}
    a{{color:red}}
    </style>

    <div class="card">
        <h2>🏥 Hospital PRO MAX</h2>

        👤 {user.username} <br>
        🟢 Онлайн: {len(online_users)} <br>

        <div class="box">💰 {user.coins}</div>
        <div class="box">💎 {user.diamonds}</div>
        <div class="box">⭐ LVL {user.level}</div>

        <p>XP</p>
        <div class="bar"><div class="fill"></div></div>

        <br>

        <a href="/patients"><button>🧑‍⚕ Пациенты</button></a>
        <a href="/garage"><button>🚑 Автопарк</button></a>
        <a href="/operating"><button>🏥 Операционная</button></a>
        <a href="/lab"><button>🧪 Лаборатория</button></a>
        <a href="/alliance"><button>🏛 Союзы</button></a>
        <a href="/chat"><button>💬 Чат</button></a>

        <br><br>
        <a href="/logout">🚪 выход</a>
    </div>
    """

# ================= REGISTER =================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "exists"

        db.session.add(User(username=u, password=p))
        db.session.commit()

        return redirect("/login")

    return """
    <style>body{background:#05070c;color:white;text-align:center}</style>
    <h2>🆕 REG</h2>
    <form method="post">
    <input name="username"><br>
    <input name="password"><br>
    <button>create</button>
    </form>
    """

# ================= LOGIN =================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if not user:
            return "error"

        session["user"] = u
        online_users.add(u)

        return redirect("/")

    return "<form method='post'><input name='username'><input name='password'><button>login</button></form>"

# ================= PATIENTS =================
@app.route("/patients")
def show_patients():
    random_list = random.sample(patients, 20)

    html = "<h2>🧑‍⚕ Пациенты (из 50k)</h2>"

    for p in random_list:
        html += f"""
        <div style='border:1px solid red;margin:5px;padding:5px'>
        {p['name']} | HP:{p['hp']}
        <a href='/treat/{p['id']}'>лечить</a>
        </div>
        """

    return html

# ================= TREAT =================
@app.route("/treat/<int:pid>")
def treat(pid):
    user = User.query.filter_by(username=session["user"]).first()
    user.xp += 5
    user.coins += 10
    db.session.commit()

    return redirect("/patients")

# ================= GARAGE =================
@app.route("/garage")
def garage():
    return """
    <h2>🚑 Автопарк</h2>
    <a href="/buy/ambulance">Купить Ambulance</a><br>
    <a href="/send_call">📞 Вызов пациента</a>
    """

@app.route("/buy/<car>")
def buy(car):
    user = User.query.filter_by(username=session["user"]).first()

    if user.coins >= cars[car]:
        user.coins -= cars[car]
        user_cars.setdefault(user.username, []).append(car)
        db.session.commit()

    return redirect("/garage")

# ================= OPERATING =================
@app.route("/operating")
def operating():
    roll = random.randint(1, 6)
    return f"""
    <h2>🏥 Операционная</h2>
    🎲 Кубик: {roll}
    """

# ================= LAB =================
@app.route("/lab")
def lab():
    return """
    <h2>🧪 Лаборатория</h2>
    <a href='/analyze'>Взять анализ</a><br>
    <a href='/heal'>Лечить</a>
    """

@app.route("/analyze")
def analyze():
    return "📊 анализ взят"

@app.route("/heal")
def heal():
    return "💉 пациент вылечен"

# ================= ALLIANCE =================
@app.route("/alliance")
def alliance():
    return """
    <h2>🏛 Союзы</h2>
    <a href='/create_alliance'>Создать (500💎)</a><br>
    """

@app.route("/create_alliance")
def create_alliance():
    user = User.query.filter_by(username=session["user"]).first()

    if user.diamonds >= 500:
        user.diamonds -= 500
        user.alliance = "Alliance#" + user.username
        db.session.commit()

    return redirect("/alliance")

# ================= CHAT =================
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        messages.append(session["user"] + ": " + request.form["msg"])

    return "<br>".join(messages[-30:]) + "<form method='post'><input name='msg'><button>send</button></form>"

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    online_users.discard(session.get("user"))
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

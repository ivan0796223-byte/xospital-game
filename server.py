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

# ================= 50 000 PATIENTS =================
def patient(pid):
    random.seed(pid)
    return {
        "id": pid,
        "name": f"🧍 Patient #{pid}",
        "hp": random.randint(30, 100),
        "room": random.randint(1, 50)
    }

# ================= CARS =================
CARS = {
    "ambulance": 1000,
    "helicopter": 5000,
    "vip": 2000
}

user_cars = {}
calls = {}

# ================= ALLIANCE =================
alliances = {}

# ================= USER =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=200)
    diamonds = db.Column(db.Integer, default=50)

    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    alliance = db.Column(db.String(80), default="")

with app.app_context():
    db.create_all()

# ================= UI STYLE =================
STYLE = """
<style>
body{
    margin:0;
    font-family:Arial;
    background:#05070c;
    color:white;
}
.card{
    background:#0f1722;
    border:2px solid red;
    margin:10px;
    padding:12px;
    border-radius:15px;
}
button{
    background:red;
    color:white;
    border:none;
    padding:8px;
    margin:5px;
    border-radius:10px;
}
a{color:red}
.icon{
    width:45px;height:45px;
    border-radius:50%;
    border:2px solid red;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    margin:4px;
}
.bar{background:#222;height:10px;border-radius:20px}
.fill{background:red;height:10px}
h2{border-left:5px solid red;padding-left:10px}
</style>
"""

# ================= HOME =================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    xp = user.xp % 100

    return STYLE + f"""
    <div class="card">
        <h2>🏥 HOSPITAL MMO</h2>

        👤 {user.username}<br>
        🟢 Онлайн: {len(online_users)}<br>

        <div class="icon">✚</div>

        <div class="card">
            💰 {user.coins} | 💎 {user.diamonds} | ⭐ {user.level}
        </div>

        <div class="bar"><div class="fill" style="width:{xp}%"></div></div>

        <br>

        <a href="/patients"><button>🧍 Пациенты</button></a>
        <a href="/garage"><button>🚑 Автопарк</button></a>
        <a href="/operating"><button>🏥 Операционная</button></a>
        <a href="/lab"><button>🧪 Лаборатория</button></a>
        <a href="/exchange"><button>💱 Обменник</button></a>
        <a href="/alliance"><button>🏛 Союзы</button></a>
        <a href="/chat"><button>💬 Чат</button></a>
        <a href="/rooms"><button>🏨 Палаты</button></a>

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

    return STYLE + """
    <div class='card'>
    <h2>🆕 REG</h2>
    <form method='post'>
    <input name='username'><br>
    <input name='password'><br>
    <button>create</button>
    </form>
    </div>
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

    return STYLE + "<div class='card'><form method='post'><input name='username'><input name='password'><button>login</button></form></div>"

# ================= PATIENTS =================
@app.route("/patients")
def patients():
    html = STYLE + "<div class='card'><h2>🧍 Пациенты (50 000)</h2>"

    for i in random.sample(range(50000), 10):
        p = patient(i)

        html += f"""
        <div class='card'>
            {p['name']}<br>
            ❤️ {p['hp']} | 🏨 {p['room']}<br>
            <a href='/treat/{p['id']}'><button>лечить</button></a>
        </div>
        """

    return html + "</div>"

@app.route("/treat/<int:pid>")
def treat(pid):
    user = User.query.filter_by(username=session["user"]).first()
    user.xp += 10
    user.coins += 20
    db.session.commit()
    return redirect("/patients")

# ================= GARAGE =================
@app.route("/garage")
def garage():
    return STYLE + """
    <div class='card'>
    <h2>🚑 Автопарк</h2>

    <a href='/buy/ambulance'><button>Купить Ambulance</button></a>
    <a href='/call'><button>📞 Вызов пациента</button></a>
    </div>
    """

@app.route("/buy/<car>")
def buy(car):
    user = User.query.filter_by(username=session["user"]).first()

    if user.coins >= CARS[car]:
        user.coins -= CARS[car]
        user_cars.setdefault(user.username, []).append(car)
        db.session.commit()

    return redirect("/garage")

@app.route("/call")
def call():
    pid = random.randint(0, 49999)
    calls[pid] = "active"
    return f"📞 вызов #{pid}"

# ================= OPERATING =================
@app.route("/operating")
def operating():
    roll = random.randint(1, 6)
    return STYLE + f"""
    <div class='card'>
    <h2>🏥 Операционная</h2>
    🎲 кубик: {roll}
    </div>
    """

# ================= LAB =================
@app.route("/lab")
def lab():
    return STYLE + """
    <div class='card'>
    <h2>🧪 Лаборатория</h2>
    <a href='/analyze'><button>анализ</button></a>
    <a href='/heal'><button>лечить</button></a>
    </div>
    """

@app.route("/analyze")
def analyze():
    return "📊 анализ"

@app.route("/heal")
def heal():
    return "💉 лечение"

# ================= EXCHANGE =================
@app.route("/exchange")
def exchange():
    return STYLE + "<div class='card'><h2>💱 обменник</h2></div>"

# ================= ALLIANCE =================
@app.route("/alliance")
def alliance():
    return STYLE + """
    <div class='card'>
    <h2>🏛 Союзы</h2>
    <a href='/create_alliance'><button>создать (500💎)</button></a>
    <a href='/zags'><button>ЗАГС</button></a>
    </div>
    """

@app.route("/create_alliance")
def create_alliance():
    user = User.query.filter_by(username=session["user"]).first()

    if user.diamonds >= 500:
        user.diamonds -= 500
        user.alliance = "AL_" + user.username
        db.session.commit()

    return redirect("/alliance")

@app.route("/zags")
def zags():
    return STYLE + "<div class='card'>💍 ЗАГС союзов</div>"

# ================= ROOMS =================
@app.route("/rooms")
def rooms():
    return STYLE + "<div class='card'><h2>🏨 Палаты</h2></div>"

# ================= CHAT =================
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        messages.append(session["user"] + ": " + request.form["msg"])

    return STYLE + "<div class='card'><h2>💬 чат</h2>" + "<br>".join(messages[-20:]) + """
    <form method='post'>
    <input name='msg'>
    <button>send</button>
    </form>
    </div>
    """

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    online_users.discard(session.get("user"))
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

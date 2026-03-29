from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret123"

db = SQLAlchemy(app)

# ===== MODEL =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# ===== FIX DB =====
with app.app_context():
    db.create_all()

# ===== REGISTER =====
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                return "Введите логин и пароль"

            existing = User.query.filter_by(username=username).first()
            if existing:
                return "Пользователь уже существует"

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

        except Exception as e:
            db.session.rollback()
            return f"Ошибка: {str(e)}"

    return render_template("register.html")

# ===== LOGIN =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/")

        return "Неверный логин"

    return render_template("login.html")

# ===== HOME =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return f"""
    <h2>Добро пожаловать, {user.username}</h2>
    <a href='/logout'>Выйти</a>
    """

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== RUN =====

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    coins = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=5)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    text = db.Column(db.Text)

with app.app_context():
    db.create_all()

online = {}

def add_exp(u, val):
    u.exp += val
    if u.exp >= u.level * 100:
        u.level += 1
        u.exp = 0

# ===== AUTH =====
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if not u or not p:
            return "Введите данные"

        if User.query.filter_by(username=u).first():
            return "Уже существует"

        db.session.add(User(username=u, password=p))
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        user = User.query.filter_by(username=u, password=p).first()

        if user:
            session["user_id"] = user.id
            online[user.id] = time.time()
            return redirect("/")

        return "Ошибка входа"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== MAIN =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    u = User.query.get(session["user_id"])
    return render_template("index.html", user=u)

@app.route("/reward")
def reward():
    u = User.query.get(session["user_id"])
    u.coins += 100
    add_exp(u, 20)
    db.session.commit()
    return redirect("/")

# ===== CHAT =====
@app.route("/chat", methods=["GET","POST"])
def chat():
    u = User.query.get(session["user_id"])

    if request.method == "POST":
        text = request.form.get("text")
        if text:
            db.session.add(Message(user=u.username, text=text))
            db.session.commit()

    return render_template("chat.html", messages=Message.query.all())

# ===== PATIENTS =====
@app.route("/patients")
def patients():
    patients = []
    for _ in range(12):
        pid = random.randint(1, 100000)
        patients.append({
            "id": pid,
            "name": f"Пациент {pid}",
            "status": random.choice(["stable","critical","waiting"])
        })
    return render_template("patients.html", patients=patients)

@app.route("/select/<int:pid>")
def select(pid):
    session["patient"] = pid
    return redirect("/patients")

@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Машина выехала к пациенту {pid}"

# ===== SURGERY =====
@app.route("/surgery")
def surgery():
    roll = random.randint(1,6)
    result = "❌ Провал" if roll<=2 else "⚠ Стабильно" if roll<=5 else "✅ Успех"
    return render_template("surgery.html", roll=roll, result=result)

# ===== LAB =====
@app.route("/lab")
def lab():
    return f"🧪 Диагноз: {random.choice(['Вирус','Здоров','Инфекция'])}"

# ===== SHOP =====
@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/

# ===== ONLINE =====
@

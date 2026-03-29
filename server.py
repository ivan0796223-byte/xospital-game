from flask import Flask, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================== USER ==================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# создаём таблицы
with app.app_context():
    db.create_all()

# ================== HOME ==================
@app.route("/")
def home():
    if "user" in session:
        return f"🏥 Hospital Game | {session['user']}"
    return redirect("/login")

# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "❌ Пользователь уже существует"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return """
    <h2>Регистрация</h2>
    <form method="post">
        <input name="username" placeholder="Логин"><br>
        <input name="password" type="password" placeholder="Пароль"><br>
        <button>Зарегистрироваться</button>
    </form>
    """

# ================== LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user"] = user.username
            return redirect("/")
        return "❌ Неверный логин или пароль"

    return """
    <h2>Вход</h2>
    <form method="post">
        <input name="username"><br>
        <input name="password" type="password"><br>
        <button>Войти</button>
    </form>
    """

# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

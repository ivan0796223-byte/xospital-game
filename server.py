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
if __name__ == "__main__":
    app.run(debug=True)

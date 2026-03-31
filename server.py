from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "secret"

users = {}
online_players = 5

patients = [{"id": i, "name": f"Пациент {i}"} for i in range(1, 2001)]

# ---------------- ГЛАВНАЯ ----------------

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# ---------------- РЕГИСТРАЦИЯ ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            return "Заполни все поля"

        if login in users:
            return "Логин уже занят"

        users[login] = {
            "password": password,
            "coins": 1000,
            "diamonds": 500,
            "exp": 0,
            "level": 1
        }

        return redirect("/login")

    return render_template("register.html")

# ---------------- ВХОД ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login not in users:
            return "Пользователь не найден"

        if users[login]["password"] != password:
            return "Неверный пароль"

        session["user"] = login
        return redirect("/dashboard")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = users[session["user"]]
    return render_template("dashboard.html", user=user, online=online_players)

# ---------------- ПАЦИЕНТЫ ----------------

@app.route("/patients")
def patients_page():
    if "user" not in session:
        return redirect("/login")

    return render_template("patients.html", patients=patients)

# ---------------- ОПЕРАЦИОННАЯ ----------------

@app.route("/operating")
def operating():
    if "user" not in session:
        return redirect("/login")

    result = random.randint(1, 6)
    return render_template("operating.html", dice=result)

# ---------------- ЛАБОРАТОРИЯ ----------------

@app.route("/lab")
def lab():
    if "user" not in session:
        return redirect("/login")

    return render_template("lab.html")

# ---------------- АВТОПАРК ----------------

@app.route("/garage")
def garage():
    if "user" not in session:
        return redirect("/login")

    return render_template("garage.html")

# ---------------- МАГАЗИН ----------------

@app.route("/shop")
def shop():
    if "user" not in session:
        return redirect("/login")

    return render_template("shop.html")

# ---------------- СОЮЗ ----------------

@app.route("/alliance", methods=["GET", "POST"])
def alliance():
    if "user" not in session:
        return redirect("/login")

    message = ""

    if request.method == "POST":
        user = users[session["user"]]

        if user["diamonds"] >= 500:
            user["diamonds"] -= 500
            message = "Союз создан!"
        else:
            message = "Недостаточно алмазов!"

    return render_template("alliance.html", message=message)

# ---------------- ДОКТОР ----------------

@app.route("/doctor")
def doctor():
    if "user" not in session:
        return redirect("/login")

    return render_template("doctor.html")

# ---------------- ВЫХОД ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- ЗАПУСК ----------------

if __name__ == "__main__":
    app.run(debug=True)

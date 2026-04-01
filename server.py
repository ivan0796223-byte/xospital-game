from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = {}

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
            return "Логин занят"

        users[login] = {
            "password": password,
            "coins": 1000,
            "diamonds": 500
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
    return render_template("dashboard.html", user=user)

# ---------------- ВЫХОД ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- ЗАПУСК ----------------
if __name__ == "__main__":
    app.run(debug=True)

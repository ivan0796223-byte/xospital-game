from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"

# ====== ДАННЫЕ ======
game = {
    "messages": [],
    "users": {}
}

# ====== ГЛАВНАЯ ======
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    user = game["users"][session["user"]]
    return render_template("index.html", user=user)

# ====== ЛОГИН (НЕ ТРОГАЕМ ЛОГИКУ, ТОЛЬКО ЧИТАЕМ) ======
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        if username in game["users"]:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return "❌ Нет такого пользователя"

    return render_template("login.html")

# ====== РЕГИСТРАЦИЯ (НОВАЯ, ПРАВИЛЬНАЯ) ======
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]

        if username in game["users"]:
            return "❌ Уже существует"

        game["users"][username] = {
            "coins": 100,
            "diamonds": 5
        }

        session["user"] = username
        return redirect(url_for("index"))

    return render_template("register.html")

# ====== ЧАТ ======
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        msg = request.form["msg"]
        game["messages"].append(f"{session['user']}: {msg}")

    return render_template("chat.html", game=game)

# ====== ОБМЕННИК ======
@app.route("/exchange")
def exchange():
    user = game["users"][session["user"]]

    if user["coins"] >= 50:
        user["coins"] -= 50
        user["diamonds"] += 1

    return render_template("exchange.html", user=user)

# ====== МАГАЗИН ======
@app.route("/shop")
def shop():
    return render_template("shop.html")

# ====== ЛАБА ======
@app.route("/lab")
def lab():
    result = "🦠 Вирус обнаружен"
    return render_template("lab.html", result=result)

# ====== ДИАГНОСТИКА ======
@app.route("/diagnosis")
def diagnosis():
    return render_template("diagnosis.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"

# ====== ИГРОВЫЕ ДАННЫЕ ======
game = {
    "coins": 100,
    "diamonds": 10,
    "messages": [],
    "users": {},
    "lab_result": "Нет анализов"
}

# ====== ГЛАВНАЯ ======
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", game=game)

# ====== РЕГИСТРАЦИЯ / ЛОГИН ======
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        game["users"][username] = {"coins": 100, "diamonds": 5}
        return redirect(url_for("index"))
    return render_template("login.html")

# ====== ЧАТ ======
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = request.form["msg"]
        user = session.get("user", "anon")
        game["messages"].append(f"{user}: {msg}")
    return render_template("chat.html", game=game)

# ====== ОБМЕННИК ======
@app.route("/exchange")
def exchange():
    user = session["user"]
    u = game["users"][user]
    if u["coins"] >= 50:
        u["coins"] -= 50
        u["diamonds"] += 1
    return render_template("exchange.html", user=u)

# ====== МАГАЗИН ======
@app.route("/shop")
def shop():
    return render_template("shop.html")

# ====== ЛАБОРАТОРИЯ ======
@app.route("/lab")
def lab():
    game["lab_result"] = "Анализ: вирус найден 🦠"
    return render_template("lab.html", game=game)

# ====== ДИАГНОСТИКА ======
@app.route("/diagnosis")
def diagnosis():
    return render_template("diagnosis.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Игрок
player = {
    "money": 1000,
    "exp": 0
}

# Главная
@app.route("/")
def index():
    return render_template("index.html", player=player)

# Пациенты
@app.route("/patients")
def patients():
    return render_template("patients.html", player=player)

# Действия
@app.route("/action", methods=["POST"])
def action():
    action = request.form.get("action")

    if action == "heal1":
        player["money"] += 100
        player["exp"] += 10

    elif action == "heal2":
        player["money"] += 200
        player["exp"] += 20

    elif action == "heal3":
        player["money"] += 300
        player["exp"] += 30

    return redirect(url_for("patients"))

if __name__ == "__main__":
    app.run(debug=True)

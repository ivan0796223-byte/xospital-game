
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Игровые данные (простые)
player = {
    "exp": 0,
    "money": 100
}

@app.route("/")
def home():
    return render_template("index.html", player=player)

@app.route("/lab")
def lab():
    return render_template("lab.html", player=player)

@app.route("/game")
def game():
    return render_template("game.html", player=player)

# ДЕЙСТВИЕ (кнопка)
@app.route("/action", methods=["POST"])
def action():
    data = request.get_json()
    act = data.get("action")

    if act == "heal":
        player["exp"] += 10
        player["money"] += 20

    elif act == "research":
        player["exp"] += 20
        player["money"] -= 10

    return jsonify(player)

if __name__ == "__main__":
    app.run(debug=True)

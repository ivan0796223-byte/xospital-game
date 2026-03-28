from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 💰 начальные данные игрока
game = {
    "money": 50000,
    "location": "Лобби",
    "patients": ["Иванов", "Петров", "Сидоров"],
    "chat": []
}

@app.route("/")
def home():
    return render_template("index.html", game=game)

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    act = data.get("action")

    if act == "hospital":
        game["location"] = "Больница"
        msg = "Ты перешёл в больницу"
    elif act == "garage":
        game["location"] = "Автопарк"
        msg = "Ты в автопарке"
    elif act == "chat":
        msg = "Открыт чат"
    else:
        msg = "Неизвестное действие"

    game["chat"].append(msg)

    return jsonify(game)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 💰 начальные данные игрока
game = {
    "money": 50000,
    "location": "Лобби",
    "patients": ["Иванов", "Петров", "Сидоров"],
    "chat": []
}

@app.route("/")
def home():
    return render_template("index.html", game=game)

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    act = data.get("action")

    if act == "hospital":
        game["location"] = "Больница"
        msg = "Ты перешёл в больницу"
    elif act == "garage":
        game["location"] = "Автопарк"
        msg = "Ты в автопарке"
    elif act == "chat":
        msg = "Открыт чат"
    else:
        msg = "Неизвестное действие"

    game["chat"].append(msg)

    return jsonify(game)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

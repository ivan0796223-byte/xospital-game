from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

player = {
    "money": 100,
    "xp": 0,
    "diamonds": 5,
    "level": 1
}

selected_patient = {"id": None}

chat = []

names = ["Алекс", "Мария", "Иван", "Олег", "Анна", "Дима", "София", "Макс"]

patients = [
    {
        "id": i,
        "name": random.choice(names) + f" #{i}",
        "hp": random.randint(40, 100)
    }
    for i in range(1, 5001)
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/lab")
def lab():
    return render_template("lab.html")


@app.route("/data")
def data():
    return jsonify({
        "player": player,
        "patients": patients,
        "selected": selected_patient
    })


@app.route("/select", methods=["POST"])
def select():
    data = request.get_json(force=True)
    selected_patient["id"] = int(data["id"])
    return jsonify({"ok": True})


@app.route("/action/<act>", methods=["POST"])
def action(act):
    data = request.get_json(force=True)
    pid = int(data["id"])

    for p in patients:
        if p["id"] == pid:

            if act == "heal":
                p["hp"] = min(100, p["hp"] + 20)
                player["money"] += 10
                player["xp"] += 5
                player["diamonds"] += 1

            elif act == "lab":
                player["xp"] += 10
                player["diamonds"] += 2

            break

    need = player["level"] * 50
    if player["xp"] >= need:
        player["level"] += 1
        player["xp"] = 0

    return jsonify({"ok": True})


# 💬 ЧАТ
@app.route("/chat/send", methods=["POST"])
def chat_send():
    data = request.get_json(force=True)

    chat.append({"text": data["text"]})

    if len(chat) > 50:
        chat.pop(0)

    return jsonify({"ok": True})


@app.route("/chat/get")
def chat_get():
    return jsonify(chat)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

player = {
    "money": 100,
    "diamonds": 5,
    "xp": 0,
    "level": 1
}

patients = [
    {"id": 1, "name": "Пациент 1", "hp": 100},
    {"id": 2, "name": "Пациент 2", "hp": 80}
]

selected = {"id": None}
chat = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify({
        "player": player,
        "patients": patients,
        "selected": selected
    })

@app.route("/select", methods=["POST"])
def select():
    selected["id"] = request.json["id"]
    return jsonify({"ok": True})

@app.route("/action/<type>", methods=["POST"])
def action(type):
    for p in patients:
        if p["id"] == request.json["id"]:
            if type == "heal":
                p["hp"] += 10
                player["xp"] += 5
            if type == "lab":
                player["money"] += 10
                player["xp"] += 10

    if player["xp"] >= player["level"] * 50:
        player["level"] += 1

    return jsonify({"ok": True})

@app.route("/chat/get")
def chat_get():
    return jsonify(chat)

@app.route("/chat/send", methods=["POST"])
def chat_send():
    chat.append({"text": request.json["text"]})
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

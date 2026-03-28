from flask import Flask, render_template, request, jsonify, session
import os
import random

app = Flask(__name__)
app.secret_key = "xospital-key"

users = {}

def create_user(name):
    users[name] = {
        "money": 50000,
        "diamonds": 0,
        "level": 1,
        "xp": 0,
        "selected_patient": None,
        "patients": []
    }

    # создаём много пациентов (пример)
    for i in range(50):  # можно 1000000, но лучше 50-200
        users[name]["patients"].append({
            "id": i,
            "name": f"Пациент {i}",
            "orvi": random.randint(50, 100)
        })

@app.route("/")
def home():
    if "user" not in session:
        return render_template("login.html")

    user = session["user"]

    if user not in users:
        create_user(user)

    return render_template("index.html", user=users[user], name=user)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "empty"}), 400

    session["user"] = username

    if username not in users:
        create_user(username)

    return jsonify({"ok": True})

@app.route("/select_patient", methods=["POST"])
def select_patient():
    user = users[session["user"]]
    pid = int(request.json.get("id"))

    for p in user["patients"]:
        if p["id"] == pid:
            user["selected_patient"] = p

    return jsonify(user)

@app.route("/treat", methods=["POST"])
def treat():
    user = users[session["user"]]

    if not user["selected_patient"]:
        return jsonify(user)

    p = user["selected_patient"]

    p["orvi"] = max(0, p["orvi"] - 10)

    user["xp"] += 10
    user["diamonds"] += 1

    if user["xp"] >= 100:
        user["level"] += 1
        user["xp"] = 0

    return jsonify(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

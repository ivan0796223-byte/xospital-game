from flask import Flask, render_template, request, jsonify, session
import os, random

app = Flask(__name__)
app.secret_key = "secret"

users = {}

def create_user(name, password):
    users[name] = {
        "password": password,
        "money": 50000,
        "diamonds": 0,
        "xp": 0,
        "level": 1,
        "selected_patient": None,
        "chat": [],
        "cars": ["🚑", "🚗"],
        "patients": []
    }

    for i in range(20):
        users[name]["patients"].append({
            "id": i,
            "name": f"Пациент {i}",
            "orvi": random.randint(50,100)
        })

@app.route("/")
def home():
    if "user" not in session:
        return render_template("login.html")
    return render_template("index.html", user=users[session["user"]], name=session["user"])

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    password = data["password"]

    create_user(name, password)
    session["user"] = name
    return jsonify({"ok": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data["name"]
    password = data["password"]

    if name in users and users[name]["password"] == password:
        session["user"] = name
        return jsonify({"ok": True})
    return jsonify({"error": "wrong"}), 400

@app.route("/select_patient", methods=["POST"])
def select_patient():
    user = users[session["user"]]
    pid = int(request.json["id"])

    for p in user["patients"]:
        if p["id"] == pid:
            user["selected_patient"] = p

    return jsonify(user)

@app.route("/treat", methods=["POST"])
def treat():
    user = users[session["user"]]

    if user["selected_patient"]:
        user["selected_patient"]["orvi"] -= 10

    user["xp"] += 10
    user["diamonds"] += 1

    if user["xp"] >= 100:
        user["level"] += 1
        user["xp"] = 0

    return jsonify(user)

@app.route("/chat", methods=["POST"])
def chat():
    user = users[session["user"]]
    msg = request.json["msg"]
    user["chat"].append(msg)
    return jsonify(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

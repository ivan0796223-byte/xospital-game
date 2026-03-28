from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "xospital-key"

users = {}

def create_user(name):
    users[name] = {
        "money": 50000,
        "diamonds": 0,
        "orvi": 100,
        "level": 1,
        "xp": 0
    }

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

@app.route("/action", methods=["POST"])
def action():
    if "user" not in session:
        return jsonify({"error": "no user"}), 401

    user = users[session["user"]]

    user["xp"] += 20
    user["diamonds"] += 1
    user["orvi"] = max(0, user["orvi"] - 8)

    if user["xp"] >= 100:
        user["level"] += 1
        user["xp"] = 0

    return jsonify(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

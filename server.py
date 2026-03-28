from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "secret-key"

# простая база (в памяти)
users = {}

@app.route("/")
def home():
    if "user" not in session:
        return render_template("login.html")
    return render_template("index.html", user=users[session["user"]])

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]

    users[username] = {
        "money": 50000,
        "diamonds": 0,
        "orvi": 100,
        "level": 1,
        "xp": 0
    }

    session["user"] = username
    return jsonify({"ok": True})

@app.route("/action", methods=["POST"])
def action():
    user = users[session["user"]]

    user["xp"] += 10
    user["diamonds"] += 1
    user["orvi"] -= 5

    if user["xp"] >= 100:
        user["level"] += 1
        user["xp"] = 0

    return jsonify(user)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

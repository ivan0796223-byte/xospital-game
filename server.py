from flask import Flask, render_template, request, jsonify, session
import os, random

app = Flask(__name__)
app.secret_key = "xospital"

users = {}

# ---------- USER ----------
def create_user(name, password):
    users[name] = {
        "password": password,
        "money": 50000,
        "diamonds": 0,
        "xp": 0,
        "level": 1,
        "selected_patient": None,
        "chat": [],
        "cars": ["🚑", "🚗", "🚓"],
    }

def get_patient(i):
    return {
        "id": i,
        "name": f"Пациент {i}",
        "orvi": (i * 7) % 100
    }

# ---------- ROUTES ----------
@app.route("/")
def home():
    if "user" not in session:
        return render_template("login.html")
    u = users[session["user"]]
    return render_template("index.html", user=u, name=session["user"])

@app.route("/register", methods=["POST"])
def register():
    d = request.json
    create_user(d["name"], d["password"])
    session["user"] = d["name"]
    return jsonify(ok=True)

@app.route("/login", methods=["POST"])
def login():
    d = request.json
    u = d["name"]
    if u in users and users[u]["password"] == d["password"]:
        session["user"] = u
        return jsonify(ok=True)
    return jsonify(error="bad"), 400

# ---------- PATIENT ----------
@app.route("/select_patient", methods=["POST"])
def select_patient():
    u = users[session["user"]]
    pid = int(request.json["id"])
    u["selected_patient"] = get_patient(pid)
    return jsonify(ok=True)

@app.route("/treat", methods=["POST"])
def treat():
    u = users[session["user"]]
    if u["selected_patient"]:
        u["selected_patient"]["orvi"] -= 10

    u["xp"] += 15
    u["diamonds"] += 1

    if u["xp"] >= 100:
        u["level"] += 1
        u["xp"] = 0

    return jsonify(u)

# ---------- CHAT ----------
@app.route("/chat", methods=["POST"])
def chat():
    u = users[session["user"]]
    msg = request.json["msg"]
    u["chat"].append(msg)
    return jsonify(ok=True)

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

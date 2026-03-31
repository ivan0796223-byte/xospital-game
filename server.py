from flask import Flask, request, jsonify, redirect, session
import random
import datetime

app = Flask(__name__)
app.secret_key = "xospital_pro_key"

# =========================
# 👤 ДАННЫЕ ИГРЫ
# =========================

users = {}
alliances = {}

players_online = 12  # эмуляция онлайн

patients = [
    {
        "id": i,
        "name": f"Пациент #{i}",
        "event": random.choice(["авария", "болезнь", "операция", "инфекция"])
    }
    for i in range(1, 2001)
]

# =========================
# 🧍 РЕГИСТРАЦИЯ / ВХОД
# =========================

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]

    if username in users:
        return jsonify({"error": "exists"})

    users[username] = {
        "password": data["password"],
        "coins": 100,
        "diamonds": 10,
        "exp": 0,
        "level": 1,
        "patients": []
    }

    return jsonify({"ok": True})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.get(data["username"])

    if not user or user["password"] != data["password"]:
        return jsonify({"error": "wrong"})

    session["user"] = data["username"]
    return jsonify({"ok": True})


# =========================
# 👤 ПРОФИЛЬ
# =========================

@app.route("/profile")
def profile():
    u = session.get("user")
    if not u:
        return jsonify({"error": "not logged"})

    return jsonify(users[u])


# =========================
# 🏥 ПАЦИЕНТЫ (2000)
# =========================

@app.route("/patients")
def get_patients():
    return jsonify(patients)


@app.route("/select_patient", methods=["POST"])
def select_patient():
    u = session.get("user")
    if not u:
        return jsonify({"error": "not logged"})

    pid = request.json["id"]

    users[u]["patients"].append(pid)

    return jsonify({"selected": pid})


# =========================
# ⚕️ ОПЕРАЦИОННАЯ (КУБИКИ)
# =========================

@app.route("/operation", methods=["POST"])
def operation():
    u = session.get("user")
    if not u:
        return jsonify({"error": "not logged"})

    dice = random.randint(1, 6)

    if dice >= 4:
        users[u]["coins"] += 50
        users[u]["exp"] += 20
        result = "success"
    else:
        users[u]["coins"] += 5
        users[u]["exp"] += 5
        result = "fail"

    return jsonify({
        "dice": dice,
        "result": result,
        "player": users[u]
    })


# =========================
# 🚑 АВТОПАРК / ВЫЗОВЫ
# =========================

@app.route("/call_patient")
def call_patient():
    return jsonify(random.choice(patients))


# =========================
# 🧪 ЛАБОРАТОРИЯ
# =========================

@app.route("/lab", methods=["POST"])
def lab():
    u = session.get("user")
    if not u:
        return jsonify({"error": "not logged"})

    users[u]["exp"] += 15
    users[u]["coins"] += 10

    return jsonify(users[u])


# =========================
# 🏪 МАГАЗИН
# =========================

shop = {
    "knife": {"price": 50},
    "scanner": {"price": 100},
    "medkit": {"price": 30}
}

@app.route("/shop")
def get_shop():
    return jsonify(shop)


@app.route("/buy", methods=["POST"])
def buy():
    u = session.get("user")
    item = request.json["item"]

    if users[u]["coins"] >= shop[item]["price"]:
        users[u]["coins"] -= shop[item]["price"]
        return jsonify({"bought": item})

    return jsonify({"error": "not enough money"})


# =========================
# 🏥 СОЮЗЫ (АЛЬЯНСЫ)
# =========================

@app.route("/create_alliance", methods=["POST"])
def create_alliance():
    u = session.get("user")
    name = request.json["name"]

    alliances[name] = {
        "owner": u,
        "members": [u],
        "level": 1
    }

    return jsonify(alliances[name])


@app.route("/search_alliance")
def search_alliance():
    return jsonify(list(alliances.keys()))


# =========================
# 🔍 ПОИСК ИГРОКОВ
# =========================

@app.route("/search_player")
def search_player():
    return jsonify(list(users.keys()))


# =========================
# 🕒 ВРЕМЯ МСК
# =========================

@app.route("/time")
def time():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    return jsonify({"MSK": str(now)})


# =========================
# 👥 ОНЛАЙН ИГРОКИ
# =========================

@app.route("/online")
def online():
    return jsonify({"online": players_online + random.randint(-3, 5)})


# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

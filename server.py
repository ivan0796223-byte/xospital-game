from flask import Flask, render_template, redirect, url_for
import time

app = Flask(__name__)

# ====== ДАННЫЕ ИГРЫ ======
game = {
    "coins": 100,
    "diamonds": 10,
    "cars": {
        "Скорая №1": {"busy": False, "return_time": 0},
        "Скорая №2": {"busy": False, "return_time": 0},
    },
    "patients": [
        {"id": 1, "name": "Иван", "disease": "Аппендицит", "room": 1, "healed": False},
        {"id": 2, "name": "Олег", "disease": "Перелом", "room": 2, "healed": False},
        {"id": 3, "name": "Анна", "disease": "Грипп", "room": 3, "healed": False},
    ],
    "rooms": {
        1: "Свободна",
        2: "Свободна",
        3: "Свободна"
    }
}

# ====== ГЛАВНАЯ ======
@app.route("/")
def index():
    check_cars()
    return render_template("index.html", game=game)

# ====== ПАЦИЕНТЫ ======
@app.route("/patients")
def patients():
    return render_template("patients.html", game=game)

# ====== ПАЛАТЫ ======
@app.route("/rooms")
def rooms():
    return render_template("rooms.html", game=game)

# ====== ГАРАЖ ======
@app.route("/garage")
def garage():
    check_cars()
    return render_template("garage.html", game=game)

# ====== ОПЕРАЦИЯ ======
@app.route("/heal/<int:pid>")
def heal(pid):
    for p in game["patients"]:
        if p["id"] == pid:
            p["healed"] = True
            game["coins"] += 20
            game["diamonds"] += 1
    return redirect(url_for("patients"))

# ====== ПОЕЗДКА ======
@app.route("/send_car/<name>")
def send_car(name):
    now = time.time()
    game["cars"][name]["busy"] = True
    game["cars"][name]["return_time"] = now + 10  # 10 сек поездка
    game["coins"] += 5
    return redirect(url_for("garage"))

# ====== ПРОВЕРКА МАШИН ======
def check_cars():
    now = time.time()
    for car in game["cars"]:
        if game["cars"][car]["busy"]:
            if now >= game["cars"][car]["return_time"]:
                game["cars"][car]["busy"] = False

if __name__ == "__main__":
    app.run(debug=True)

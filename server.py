from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ===== БАЗА =====
def get_db():
    conn = sqlite3.connect("game.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        money INTEGER,
        exp INTEGER,
        diamonds INTEGER
    )
    """)
    cur = conn.execute("SELECT * FROM player")
    if cur.fetchone() is None:
        conn.execute("INSERT INTO player (money, exp, diamonds) VALUES (1000,0,10)")
    conn.commit()
    conn.close()

init_db()

def get_player():
    conn = get_db()
    player = conn.execute("SELECT * FROM player").fetchone()
    conn.close()
    return player

def update_player(money=0, exp=0, diamonds=0):
    conn = get_db()
    conn.execute("""
    UPDATE player
    SET money = money + ?, exp = exp + ?, diamonds = diamonds + ?
    """, (money, exp, diamonds))
    conn.commit()
    conn.close()

# ===== ПАЦИЕНТЫ =====
patients_list = [f"Пациент №{i}" for i in range(1, 100001)]

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    player = get_player()
    level = player["exp"] // 100
    progress = player["exp"] % 100
    return render_template("index.html", player=player, level=level, progress=progress)

# ===== ПАЦИЕНТЫ =====
@app.route("/patients")
def patients():
    player = get_player()
    page = int(request.args.get("page", 1))
    per_page = 20

    start = (page - 1) * per_page
    end = start + per_page

    return render_template(
        "patients.html",
        player=player,
        patients=patients_list[start:end],
        page=page,
        total=len(patients_list)
    )

@app.route("/heal", methods=["POST"])
def heal():
    update_player(100, 10)
    return redirect(url_for("patients"))

# ===== ПАЛАТЫ =====
@app.route("/ward")
def ward():
    return render_template("ward.html", player=get_player())

@app.route("/ward_action", methods=["POST"])
def ward_action():
    a = request.form.get("action")
    if a == "clean":
        update_player(exp=10)
    elif a == "check":
        update_player(exp=5)
    elif a == "talk":
        update_player(exp=3)
    return redirect(url_for("ward"))

# ===== ОПЕРАЦИОННАЯ =====
@app.route("/surgery")
def surgery():
    return render_template("surgery.html", player=get_player())

@app.route("/operate", methods=["POST"])
def operate():
    update_player(500, 50, 1)
    return redirect(url_for("surgery"))

# ===== АВТОПАРК =====
@app.route("/cars")
def cars():
    return render_template("cars.html", player=get_player())

@app.route("/buy_car", methods=["POST"])
def buy_car():
    update_player(money=-500)
    return redirect(url_for("cars"))

# ===== ЧАТ =====
messages = []

@app.route("/chat")
def chat():
    return render_template("chat.html", messages=messages, player=get_player())

@app.route("/send", methods=["POST"])
def send():
    msg = request.form.get("msg")
    if msg:
        messages.append(msg)
    return redirect(url_for("chat"))

# ===== ЗАПУСК =====
if __name__ == "__main__":
    app.run(debug=True)

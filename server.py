from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ===== DB =====
def db():
    conn = sqlite3.connect("game.db")
    conn.row_factory = sqlite3.Row
    return conn

def init():
    conn = db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        money INTEGER,
        exp INTEGER,
        diamonds INTEGER
    )
    """)
    cur = conn.execute("SELECT * FROM player")
    if not cur.fetchone():
        conn.execute("INSERT INTO player (money, exp, diamonds) VALUES (1000,0,10)")
    conn.commit()
    conn.close()

init()

def player():
    conn = db()
    p = conn.execute("SELECT * FROM player").fetchone()
    conn.close()
    return p

def update(m=0, e=0, d=0):
    conn = db()
    conn.execute("UPDATE player SET money=money+?, exp=exp+?, diamonds=diamonds+?", (m,e,d))
    conn.commit()
    conn.close()

# ===== 100k patients =====
patients_list = [f"Пациент №{i}" for i in range(1, 100001)]

selected_patient = None
messages = []

# ===== MAIN =====
@app.route("/")
def index():
    p = player()
    level = p["exp"] // 100
    progress = p["exp"] % 100
    return render_template("index.html", player=p, level=level, progress=progress)

# ===== PATIENTS =====
@app.route("/patients")
def patients():
    p = player()
    page = int(request.args.get("page", 1))
    per = 20

    start = (page-1)*per
    end = start+per

    return render_template("patients.html",
        player=p,
        patients=patients_list[start:end],
        page=page,
        total=len(patients_list)
    )

@app.route("/heal", methods=["POST"])
def heal():
    update(100,10,0)
    return redirect(url_for("patients"))

# ===== WARD =====
@app.route("/ward")
def ward():
    p = player()
    page = int(request.args.get("page", 1))
    per = 10

    start = (page-1)*per
    end = start+per

    return render_template("ward.html",
        player=p,
        patients=patients_list[start:end],
        page=page,
        total=len(patients_list),
        selected=selected_patient
    )

@app.route("/select_patient", methods=["POST"])
def select_patient():
    global selected_patient
    selected_patient = request.form.get("patient")
    return redirect(url_for("ward"))

@app.route("/ward_action", methods=["POST"])
def ward_action():
    a = request.form.get("action")
    if a == "clean":
        update(0,10,0)
    elif a == "check":
        update(0,5,0)
    elif a == "talk":
        update(0,3,0)
    return redirect(url_for("ward"))

# ===== SURGERY =====
@app.route("/surgery")
def surgery():
    return render_template("surgery.html", player=player())

@app.route("/operate", methods=["POST"])
def operate():
    update(500,50,1)
    return redirect(url_for("surgery"))

# ===== CARS =====
@app.route("/cars")
def cars():
    return render_template("cars.html", player=player())

@app.route("/buy_car", methods=["POST"])
def buy_car():
    update(-500,0,0)
    return redirect(url_for("cars"))

# ===== CHAT =====
@app.route("/chat")
def chat():
    return render_template("chat.html", messages=messages, player=player())

@app.route("/send", methods=["POST"])
def send():
    msg = request.form.get("msg")
    if msg:
        messages.append(msg)
    return redirect(url_for("chat"))

# ===== RUN =====
if __name__ == "__main__":
    app.run(debug=True)

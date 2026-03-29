return render_template("diagnosis.html")

# ===== GARAGE =====
cars = {"🚑": 1, "🚗": 2, "🚓": 3}

@app.route("/garage")
def garage():
    return render_template("garage.html", cars=cars)

@app.route("/call/<car>")
def call(car):
    pid = random.randint(1,100000)
    p = patients[pid]
    rooms.append(p)
    return redirect("/garage")

# ===== ONLINE =====
@app.route("/online")
def online():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    return f"Онлайн: {cur.fetchone()[0]}"

app.run(debug=True)

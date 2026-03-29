return render_template("diagnosis.html")

# ===== АВТОПАРК =====
@app.route("/garage")
def garage():
    now = time.time()
    for c in cars:
        if cars[c]["busy"] and now >= cars[c]["return"]:
            cars[c]["busy"] = False
    return render_template("garage.html", cars=cars)

# ===== ВЫЗОВ =====
@app.route("/call/<car>")
def call(car):
    cars[car]["busy"] = True
    cars[car]["return"] = time.time()+10

    pid = random.randint(1,100000)

    con = db()
    cur = con.cursor()

    cur.execute("UPDATE users SET coins=coins+30, exp=exp+15 WHERE username=?", (session["user"],))
    cur.execute("INSERT INTO notifications VALUES(?)", (f"🚑 Привезен пациент #{pid}",))

    con.commit()
    return redirect("/garage")

# ===== ОНЛАЙН =====
@app.route("/online")
def online():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    return f"Онлайн: {count}"

app.run(debug=True)

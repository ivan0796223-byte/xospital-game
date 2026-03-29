return render_template("operation.html", operation=operation)

# ===== ИССЛЕДОВАНИЕ =====
@app.route("/research")
def research():
    con = db()
    cur = con.cursor()

    cur.execute("UPDATE users SET coins=coins-20, exp=exp+10 WHERE coins>=20 AND username=?", (session["user"],))
    con.commit()

    result = random.choice(["Новая вакцина","Улучшение лечения","Ошибка исследования"])
    return render_template("lab.html", result=result)

# ===== ОБМЕН =====
@app.route("/exchange")
def exchange():
    con = db()
    cur = con.cursor()
    cur.execute("UPDATE users SET coins=coins-50, diamonds=diamonds+1 WHERE coins>=50 AND username=?", (session["user"],))
    con.commit()
    return redirect("/")

# ===== АВТО =====
@app.route("/garage")
def garage():
    return render_template("garage.html", cars=cars)

@app.route("/call/<car>")
def call(car):
    pid = random.randint(1,100000)
    p = next(x for x in patients if x["id"] == pid)
    rooms.append(p)
    return redirect("/garage")

# ===== ОНЛАЙН =====
@app.route("/online")
def online():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    return f"Онлайн: {cur.fetchone()[0]}"

app.run(debug=True)

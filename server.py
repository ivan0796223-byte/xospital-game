return render_template("operating.html", operation=operation)

# ================= EXCHANGE =================
@app.route("/exchange")
def exchange():
    con = db()
    cur = con.cursor()
    cur.execute("""
        UPDATE users 
        SET coins = coins - 50, diamonds = diamonds + 1 
        WHERE coins >= 50
    """)
    con.commit()
    return redirect("/")

# ================= LAB =================
@app.route("/lab")
def lab():
    return render_template("lab.html",
        result=random.choice(["🧪 Чисто", "🦠 Вирус", "⚠ Риск"])
    )

# ================= DIAGNOSIS =================
@app.route("/diagnosis")
def diagnosis():
    return render_template("diagnosis.html")

# ================= GARAGE =================
cars = ["🚑", "🚗", "🚓"]

@app.route("/garage")
def garage():
    return render_template("garage.html", cars=cars)

@app.route("/call/<car>")
def call(car):
    p = get_patient(random.randint(1, 99999))
    if p:
        rooms.append(p)
    return redirect("/garage")

# ================= ONLINE =================
@app.route("/online")
def online():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    return f"👥 Онлайн: {cur.fetchone()[0]}"

# ================= SAFE RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

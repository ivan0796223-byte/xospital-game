data.append({
            "id": pid,
            "name": f"Patient {pid}",
            "status": random.choice(["stable", "critical", "waiting"])
        })

    return render_template("patients.html", patients=data)

@app.route("/call/<int:pid>")
def call(pid):
    return f"🚑 Вызов пациента {pid}"

# =====================
# SURGERY (DICE GAME)
# =====================
@app.route("/surgery")
def surgery():
    roll = random.randint(1, 6)

    if roll <= 2:
        result = "❌ Провал"
    elif roll <= 5:
        result = "⚠ Стабильно"
    else:
        result = "✅ Успех"

    return render_template("surgery.html", roll=roll, result=result)

# =====================
# LAB
# =====================
@app.route("/lab")
def lab():
    return f"🧪 {random.choice(['Virus','Healthy','Infection','Unknown'])}"

# =====================
# EXCHANGE
# =====================
@app.route("/exchange")
def exchange():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.coins >= 500:
        user.coins -= 500
        user.diamonds += 1
        db.session.commit()
        return "Обмен выполнен"

    return "Недостаточно монет"

# =====================
# ONLINE
# =====================
@app.route("/online")
def online():
    return jsonify({"online": len(online)})

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

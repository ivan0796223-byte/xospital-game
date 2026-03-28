from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

player = {
    "money": 1000,
    "exp": 0
}

# 100000 пациентов
patients_list = [f"Пациент №{i}" for i in range(1, 100001)]

# Главная
@app.route("/")
def index():
    return render_template("index.html", player=player)

# Пациенты
@app.route("/patients")
def patients():
    page = int(request.args.get("page", 1))
    per_page = 20

    start = (page - 1) * per_page
    end = start + per_page

    current_patients = patients_list[start:end]

    return render_template(
        "patients.html",
        player=player,
        patients=current_patients,
        page=page,
        total=len(patients_list)
    )

# Лечение
@app.route("/heal", methods=["POST"])
def heal():
    player["money"] += 100
    player["exp"] += 10
    return redirect(url_for("patients"))

# Палаты
@app.route("/ward")
def ward():
    return render_template("ward.html", player=player)

# Действия в палатах
@app.route("/ward_action", methods=["POST"])
def ward_action():
    action = request.form.get("action")

    if action == "check":
        player["exp"] += 5
    elif action == "clean":
        player["exp"] += 10
    elif action == "talk":
        player["exp"] += 3

    return redirect(url_for("ward"))

if __name__ == "__main__":
    app.run(debug=True)

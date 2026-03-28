from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

player = {
    "money": 1000,
    "exp": 0
}

# Генерация 100000 пациентов
patients_list = [f"Пациент №{i}" for i in range(1, 100001)]

# Главная
@app.route("/")
def index():
    return render_template("index.html", player=player)

# Пациенты (с пагинацией)
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

# Действие
@app.route("/heal", methods=["POST"])
def heal():
    patient = request.form.get("patient")

    player["money"] += 100
    player["exp"] += 10

    return redirect(url_for("patients"))

if __name__ == "__main__":
    app.run(debug=True)

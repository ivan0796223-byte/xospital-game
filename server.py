from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("patients.html")

@app.route("/action", methods=["POST"])
def action():
    action = request.form.get("action")

    if action == "patient1":
        return "Лечение пациента 1"
    elif action == "patient2":
        return "Лечение пациента 2"
    elif action == "patient3":
        return "Лечение пациента 3"

    return "Ошибка"

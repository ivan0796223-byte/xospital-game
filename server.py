1 server from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# ===================== ДАННЫЕ =====================
patients_list = [f"Пациент №{i}" for i in range(1, 100001)]

selected_patient = None

car_calls = []

car_status = {
    "🚑 Скорая 1": "свободна",
    "🚑 Скорая 2": "свободна",
    "🚑 Скорая 3": "свободна"
}

# ===================== ГЛАВНАЯ =====================
@app.route("/")
def index():
    return render_template("index.html")

# ===================== ПАЛАТЫ =====================
@app.route("/ward")
def ward():
    page = int(request.args.get("page", 1))
    per = 10

    start = (page - 1) * per
    end = start + per

    return render_template(
        "ward.html",
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

# ===================== АВТОПАРК =====================
@app.route("/cars")
def cars():
    return render_template(
        "cars.html",
        car_calls=car_calls,
        car_status=car_status
    )

@app.route("/new_call")
def new_call():
    car_calls.append({
        "patient": random.choice(patients_list),
        "severity": random.randint(1, 10)
    })
    return redirect(url_for("cars"))

@app.route("/send_car", methods=["POST"])
def send_car():
    car = request.form.get("car")

    if car_calls and car_status[car] == "свободна":
        call = car_calls.pop(0)
        car_status[car] = f"🚨 в пути к {call['patient']} | ⚠️ {call['severity']}"

    return redirect(url_for("cars"))

@app.route("/return_car", methods=["POST"])
def return_car():
    car = request.form.get("car")
    car_status[car] = "свободна"
    return redirect(url_for("cars"))

# ===================== ЗАПУСК =====================
if __name__ == "__main__":
    app.run(debug=True)

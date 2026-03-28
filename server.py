from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"

# --- Главная ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Пациенты ---
@app.route("/patients")
def patients():
    return render_template("patients.html")

# --- Лаборатория ---
@app.route("/lab")
def lab():
    return render_template("lab.html")

# --- Операционная ---
@app.route("/operating")
def operating():
    return render_template("operating.html")

# --- Кабинет доктора ---
@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

# --- Обменник ---
@app.route("/exchange")
def exchange():
    return render_template("exchange.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

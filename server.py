
from flask import Flask, render_template

app = Flask(__name__)

# 🏠 Главная страница
@app.route("/")
def index():
    return render_template("index.html")

# 👤 Пациенты (ИСПРАВЛЕНИЕ ОШИБКИ)
@app.route("/patients")
def patients():
    return render_template("patients.html")


if __name__ == "__main__":
    app.run(debug=True)

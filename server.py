from flask import Flask, render_template

app = Flask(__name__)

# Главная
@app.route("/")
def home():
    return render_template("index.html")

# Пациенты
@app.route("/patients")
def patients():
    patients_list = ["Пациент 1", "Пациент 2", "Пациент 3"]
    return render_template("patients.html", patients=patients_list)

# Обработка 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

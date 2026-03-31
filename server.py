from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients")
def patients():
    return render_template("patients.html")

@app.errorhandler(404)
def not_found(e):
    return "Страница не найдена", 404

if __name__ == "__main__":
    app.run(debug=True)

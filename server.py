from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patients")
def patients():
    return render_template("patients.html")

@app.route("/lab")
def lab():
    return render_template("lab.html")

@app.route("/operating")
def operating():
    return render_template("operating.html")

@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

@app.route("/exchange")
def exchange():
    return render_template("exchange.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

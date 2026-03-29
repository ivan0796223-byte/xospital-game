from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "OK - Hospital Game работает"

@app.route("/rekvizity")
def rekvizity():
    return render_template("rekvizity.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

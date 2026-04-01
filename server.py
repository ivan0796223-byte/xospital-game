from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Сервер работает"

@app.route("/register")
def register():
    return "Register OK"

if __name__ == "__main__":
    app.run(debug=True)

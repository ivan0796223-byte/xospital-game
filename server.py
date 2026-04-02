from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "super_secret_key"

users = {}
patients = [{"id": i, "name": f"Пациент {i}"} for i in range(1, 2001)]

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "game.html",
        user=session.get("user"),
        coins=1000,
        diamonds=50,
        xp=120,
        next_level=200,
        online=7,
        patients=patients[:10]
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login in users and users[login] == password:
            session["user"] = login
            return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login and password:
            users[login] = password
            return redirect("/login")

    return render_template("register.html")

@app.route("/patients")
def patients_page():
    return render_template("patients.html", patients=patients[:50])

@app.route("/garage")
def garage():
    return render_template("garage.html")

@app.route("/operation")
def operation():
    dice = random.randint(1, 6)
    return render_template("operation.html", dice=dice)

@app.route("/lab")
def lab():
    return render_template("lab.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)

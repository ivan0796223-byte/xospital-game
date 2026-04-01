from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "123"

users = {}

@app.route("/")
def home():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        users[login] = password
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("login")
        return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

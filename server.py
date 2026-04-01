from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = {}

@app.route("/")
def home():
    return "Главная работает"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        users[login] = {"password": password}
        return "ЗАРЕГАНО"

    return '''
    <form method="post">
        <input name="login">
        <input name="password">
        <button type="submit">OK</button>
    </form>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "ЛОГИН ОК"

    return '''
    <form method="post">
        <input name="login">
        <input name="password">
        <button type="submit">OK</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

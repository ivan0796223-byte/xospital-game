from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = {}

@app.route("/")
def home():
    return "SERVER WORKS"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        users[login] = password
        return "REGISTER OK"

    return '''
    <h1>Регистрация</h1>
    <form method="post">
        <input name="login">
        <input name="password">
        <button type="submit">OK</button>
    </form>
    '''

if __name__ == "__main__":
    app.run()

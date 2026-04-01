from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "123"
users = {}

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        users[login] = password
        return redirect("/login")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)

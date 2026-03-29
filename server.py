from flask import Flask, render_template

app = Flask(__name__)

# ================== ГЛАВНАЯ ==================
@app.route("/")
def home():
    return "🏥 Hospital Game работает!"

# ================== РЕКВИЗИТЫ ==================
@app.route("/rekvizity")
def rekvizity():
    return render_template("rekvizity.html")


# ================== ЗАПУСК ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template

app = Flask(__name__)

# ================== ГЛАВНАЯ ==================
@app.route("/")
def home():
    return "🏥 Hospital Game работает!"

# ================== РЕКВИЗИТЫ ==================
@app.route("/rekvizity")
def rekvizity():
    return """
    <h1>Реквизиты</h1>
    <p><b>Проект:</b> Hospital Game</p>
    <p><b>Описание:</b> Онлайн игра</p>
    <p><b>Владелец:</b> Иван</p>
    <p><b>Тип:</b> игровая валюта</p>
    """

# ================== ЗАПУСК ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

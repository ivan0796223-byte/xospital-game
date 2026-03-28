 hfrom flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

# ===== МОДЕЛЬ ИГРОКА =====
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    money = db.Column(db.Integer, default=100)
    diamonds = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

# ===== ЧАТ =====
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ===== ГЛАВНАЯ =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== ДАННЫЕ ИГРОКА =====
@app.route("/data")
def data():
    player = Player.query.first()
    if not player:
        player = Player(name="Игрок")
        db.session.add(player)
        db.session.commit()

    return jsonify({
        "player": {
            "money": player.money,
            "diamonds": player.diamonds,
            "xp": player.xp,
            "level": player.level
        }
    })

# ===== ДЕНЬГИ (пример действия) =====
@app.route("/earn", methods=["POST"])
def earn():
    player = Player.query.first()
    player.money += 10
    player.xp += 5
    db.session.commit()
    return jsonify({"ok": True})

# ===== ЧАТ =====
@app.route("/chat/send", methods=["POST"])
def chat_send():
    text = request.json["text"]
    msg = Message(text=text)
    db.session.add(msg)
    db.session.commit()
    return jsonify({"ok": True})

@app.route("/chat/get")
def chat_get():
    msgs = Message.query.all()
    return jsonify([{"text": m.text} for m in msgs])

# ===== ЗАПУСК =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)ttp://127.0.0.1:5000

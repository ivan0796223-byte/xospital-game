    })
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

# ===== МОДЕЛЬ =====
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Integer, default=100)
    xp = db.Column(db.Integer, default=0)

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    player = Player.query.first()
    
    if not player:
        player = Player()
        db.session.add(player)
        db.session.commit()
    
    return render_template("index.html", player=player)

# ===== ПОЛУЧИТЬ ДАННЫЕ =====
@app.route("/get_data")
def get_data():
    player = Player.query.first()
    return jsonify({
        "money": player.money,
        "xp": player.xp
    })

# ===== ДЕЙСТВИЕ (пример кнопки) =====
@app.route("/work")
def work():
    player = Player.query.first()
    player.money += 10
    player.xp += 5
    db.session.commit()
    return jsonify({"status": "ok"})

# ===== ЗАПУСК =====
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

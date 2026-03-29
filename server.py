from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret123"

db = SQLAlchemy(app)

# ===== МОДЕЛИ =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    coins = db.Column(db.Integer, default=0)
    diamonds = db.Column(db.Integer, default=0)
    exp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    text = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ===== ГЛАВНАЯ =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("index.html", user=user)

# ===== REG =====
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if User.query.filter_by(username=u).first():
            return "USER EXISTS"

        db.session.add(User(username=u, password=p))
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

# ===== LOGIN =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session["user_id"] = user.id
            return redirect("/")
        return "WRONG LOGIN"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== НАГРАДА =====
@app.route("/reward")
def reward():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    user.coins += 100
    user.exp += 20

    if user.exp >= user.level * 100:
        user.level += 1
        user.exp = 0

    db.session.commit()
    return redirect("/")

# ===== ЧАТ =====
@app.route("/chat", methods=["GET","POST"])
def chat():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        db.session.add(Message(username=user.username, text=request.form["text"]))
        db.session.commit()

    msgs = Message.query.all()
    return render_template("chat.html", messages=msgs, user=user)

# ===== API =====
@app.route("/api/stats")
def stats():
    if "user_id" not in session:
        return jsonify({"error":"not logged"})
    u = User.query.get(session["user_id"])
    return jsonify({
        "coins": u.coins,
        "diamonds": u.diamonds,
        "exp": u.exp,
        "level": u.level
    })

# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

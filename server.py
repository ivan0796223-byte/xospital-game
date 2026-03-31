@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            login = request.form.get("login")
            password = request.form.get("password")

            if not login or not password:
                return "Заполните все поля"

            if User.query.filter_by(login=login).first():
                return "Пользователь уже существует"

            password_hash = generate_password_hash(password)
            user = User(login=login, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return redirect("/login")
    except Exception as e:
        app.logger.error(f"Ошибка при регистрации: {e}")
        return "Произошла ошибка. Попробуйте позже."

    return render_template("register.html")

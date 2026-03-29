return jsonify({"error": "not logged in"})

    user = User.query.get(session["user_id"])

    return jsonify({
        "coins": user.coins,
        "diamonds": user.diamonds,
        "exp": user.exp,
        "level": user.level
    })


# =====================
# ЗАПУСК
# =====================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

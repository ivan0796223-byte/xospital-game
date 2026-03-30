@app.route("/test-db")
def test_db():
    import os
    db_url = os.environ.get("DATABASE_URL")

    if db_url:
        return "OK: DATABASE CONNECTED"
    else:
        return "ERROR: DATABASE NOT FOUND"

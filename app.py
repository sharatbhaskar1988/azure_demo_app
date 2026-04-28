from flask import Flask
from db import get_db_connection

app = Flask(__name__)

# simple home page
@app.route("/")
def home():
    return "<h1>Hello from Azure Demo Web App</h1><p>DB connection is working via /items.</p>"

# basic health check
@app.route("/health")
def health():
    return {"status": "ok"}

# Azure SQL DB route
@app.route("/items")
def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 Id, Name FROM Items ORDER BY Id")
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({"id": row.Id, "name": row.Name})
        return {"items": result}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    # ye sirf local testing ke liye, Azure pe ignore ho jata hai
    app.run(host="0.0.0.0", port=5002, debug=True)

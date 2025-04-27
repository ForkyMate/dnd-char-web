import sqlite3
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    """
    Connection with database and makes it a dictionary
    """
    db = Path(__file__).parent / "database.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/list")
def list():
    return render_template("list.html")

@app.route("/create")
def create():
    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
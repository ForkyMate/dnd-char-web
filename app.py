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



if __name__ == "__main__":
    app.run(debug=True)
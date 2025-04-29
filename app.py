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
    conn = get_db_connection () # Pieslēdzas datubāzei

    # Izpilda SQL vaicājumu, kurš atgriež tikai vienu produktu pēc ID
    character = conn.execute(
        """
        SELECT "characters".*, "classes"."name" AS "class", "races"."name" AS "race"
        FROM characters
        LEFT JOIN "classes" ON "characters"."class_id" = "classes"."id" 
        LEFT JOIN "races" ON "characters"."race_id" = "races"."id" 
        """
    ).fetchall()
    conn. close ()
    return render_template("list.html", character=character)

@app.route("/create")
def create():
    return render_template("create.html")



if __name__ == "__main__":
    app.run(debug=True)
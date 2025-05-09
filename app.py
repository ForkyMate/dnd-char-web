from pathlib import Path
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

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
    conn = get_db_connection ()

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

@app.route("/character_<int:character_id>")
def character_show(character_id):
    conn = get_db_connection()
    character = conn.execute(
        """
        SELECT "characters".*, "classes"."name" AS "class", "races"."name" AS "race", "creators"."name" AS "creator"
        FROM characters
        LEFT JOIN "classes" ON "characters"."class_id" = "classes"."id" 
        LEFT JOIN "races" ON "characters"."race_id" = "races"."id" 
        LEFT JOIN "creators" ON "characters"."creator_id" = "creators"."id" 
        WHERE "characters"."id" = ?
        """,
        (character_id,)
    ).fetchone()
    conn.close()
    
    return render_template("character_show.html", character=character)



@app.route("/create")
def create():
    conn = get_db_connection()
    character = conn.execute("SELECT * FROM characters").fetchall()
    race = conn.execute("SELECT * FROM races").fetchall()
    clas = conn.execute("SELECT * FROM classes").fetchall()
    conn.close()

    return render_template("create.html", character=character, race=race, clas=clas)


#               datbse CRUD functions

@app.route('/submit_create', methods=['POST'])
def make_entry():
    # Get all form data
    creator_name = request.form['creator']
    char_name = request.form['character_name']
    race_id = request.form['race_id']
    class_id = request.form['class_id'] 
    level = request.form['level']
    backstory = request.form['backstory']
    image = "default.jpg"

    conn = get_db_connection()
    creators = conn.execute("SELECT * FROM creators")
    conn.close


    creator_id = -1
    for creator in creators:
        if creator_name.lower() == creator["name"].lower():
            creator_id = creator["id"]
            break
    if creator_id < 0:
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO "creators" (name)
            VALUES(?)
            """, (creator_name,)
        )
        conn.commit()
        conn.close()
        for creator in creators:
            if creator_name.lower() == creator["name"].lower():
                creator_id = creator["id"]
                break

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO "characters" (name, race_id, class_id, "level", backstory, creator_id, image)
        VALUES (?, ?, ?, ?, ?, ?, 'default.jpg')
        """, (char_name, race_id, class_id, level, creator_id, backstory)
    )
    conn.commit()
    conn.close()



    return redirect(url_for('list'))


@app.route('/update_<character_id>', methods=['GET', 'POST'])
def update(character_id):
    conn = get_db_connection()
    character = conn.execute(
        """
        SELECT "characters".*, "classes"."name" AS "class", "races"."name" AS "race", "creators"."name" AS "creator"
        FROM characters
        LEFT JOIN "classes" ON "characters"."class_id" = "classes"."id" 
        LEFT JOIN "races" ON "characters"."race_id" = "races"."id" 
        LEFT JOIN "creators" ON "characters"."creator_id" = "creators"."id" 
        WHERE "characters"."id" = ?
        """,
        (character_id,)
    ).fetchone()
    race = conn.execute("SELECT * FROM races").fetchall()
    clas = conn.execute("SELECT * FROM classes").fetchall()
    conn.close()
    
    return render_template("update.html", character=character, race=race, clas=clas)


@app.route('/submit_update', methods=['GET','POST'])
def update_entry(character_id):

    # Get all form data
    creator_name = request.form['creator']
    char_name = request.form['character_name']
    race_id = request.form['race_id']
    class_id = request.form['class_id'] 
    level = request.form['level']
    backstory = request.form['backstory']
    image = "default.jpg"



    print(creator_name)
    conn = get_db_connection()
    creators = conn.execute("SELECT * FROM creators")
    conn.close
    creator_id = -1
    for creator in creators:
        if creator_name.lower() == creator["name"].lower():
            creator_id = creator["id"]
            break
    if creator_id < 0:
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO "creators" (name)
            VALUES(?)
            """, (creator_name,)
        )
        conn.commit()
        conn.close()
        for creator in creators:
            if creator_name.lower() == creator["name"].lower():
                creator_id = creator["id"]
                break

    conn = get_db_connection()
    conn.execute(
        """
            UPDATE characters
            SET name = ?, race_id = ?, class_id = ?, creator_id = ?, backstory = ?
            WHERE id = ?
        """, (char_name, race_id, class_id, level, creator_id, backstory, character_id)
    )
    conn.commit()
    conn.close()



    return redirect(url_for('character_show', character_id))


@app.route('/delete_entry/<int:char_id>', methods=['POST'])
def delete_entry(char_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM characters WHERE id = ?', (char_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list'))
    

if __name__ == '__main__':
    app.run(debug=True)
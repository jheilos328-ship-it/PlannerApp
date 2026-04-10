import sqlite3

def connect():
    conn = sqlite3.connect("v2school.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_subject_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def create_notes_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        stuff TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE        
        )
    """)
        
    conn.commit()
    conn.close()

def add_subject(subject):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subjects (name) VALUES (?)",
        (subject,)
    )

    conn.commit()
    conn.close()

def get_subject_id(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM subjects WHERE name = ?",
        (name,)               
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None

def get_note_id(subject_id, stuff):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM notes WHERE subject_id = ? AND stuff = ?",
        (subject_id, stuff)               
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None

def add_notes(notes, subject_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO notes (subject_id, stuff) VALUES (?, ?)",
        (subject_id, notes)               
    )

    conn.commit()
    conn.close()

def update_subject_name(newname, id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("UPDATE subjects SET name = ? WHERE id = ?",
        (newname, id)               
    )

    conn.commit()
    conn.close()


def update_notes(newnotes, note_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("UPDATE notes SET stuff = ? WHERE id = ?",
        (newnotes, note_id)
    )

    conn.commit()
    conn.close()

def get_subject(id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM subjects WHERE id = ?",
        (id,)               
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None

def get_notes(subject_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT stuff FROM notes WHERE subject_id = ?",
        (subject_id,)
    )

    result = cursor.fetchall()
    conn.close()

    if result:
        return result
    return None

def get_subject_and_notes(subject_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM subjects WHERE id = ?",
        (subject_id,)               
    )

    subject_result = cursor.fetchone()

    cursor.execute("SELECT stuff FROM notes WHERE subject_id = ?",
        (subject_id,)               
    )

    notes_result = cursor.fetchall()

    if subject_result:
        notes_list = [note[0] for note in notes_result]
        if not notes_list:
            return {"subject id": subject_id, "subject name": subject_result[0], "notes": "no notes created for this subject."}
        return {"subject id": subject_id, "subject name": subject_result[0], "notes": notes_list}
    return None

def delete_subject(id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?",
        (note_id)
    )

    conn.commit()
    conn.close()

def show_all():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT")

    cursor.execute("SELECT * FROM subjects")
    subjectresults = cursor.fetchall()

    cursor.execute("SELECT * FROM stuff")
    noteresults = cursor.fetchall()

    if subjectresults:
        return {""}


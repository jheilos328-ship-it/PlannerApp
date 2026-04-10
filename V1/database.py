import sqlite3

def connect():
    return sqlite3.connect("school.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject TEXT NOT NULL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_subject_and_notes(subject, notes):      #add new subject AND notes
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO subjects (subject, notes) VALUES (?, ?)",
        (subject, notes)
    )

    conn.commit()
    conn.close()
    return True

def add_subject(subject, notes=None):       #add ONLY subject
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO subjects (subject, notes) VALUES (?, ?)",
        (subject, notes)
    )

    conn.commit()
    conn.close()
    return True

def add_notes(subject, new_notes):      #add ONLY notes
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT FROM subjects WHERE subject = ?",
    (subject,))
    result = cursor.fetchone()

    existing_notes = result[0]
    updated_notes = existing_notes + "\n" + new_notes

    cursor.execute(
        "UPDATE subjects SET notes = ? WHERE subject = ?",
    (updated_notes, subject))
    
    conn.commit()
    conn.close()
    return True

def show_all():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subjects")

    results = cursor.fetchall()

    conn.close()
    return results

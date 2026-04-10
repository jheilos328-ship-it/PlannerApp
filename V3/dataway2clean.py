import sqlite3
import os

def connect():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "v3schoolway2clean.db")
    print("Using DB:", db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_subject_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
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

def create_projects_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def create_project(name):
    try: 
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO projects (name) VALUES (?)",
            (name,)
        )
        conn.commit()

        project_id = cursor.lastrowid
        conn.close()

        return project_id
    except Exception as e:
        print("DB ERROR:", e)
        return None

def deleteproject(project_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return False

        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False
    
def show_all_projects():
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM projects")
        allprojects = cursor.fetchall()

        result = []
        for p in allprojects:
            project_id = p[0]
            project_name = p[1]

            result.append({
                "project_id": project_id,
                "project_name": project_name
            })
        conn.close()
        return result
    except Exception as e:
        print("DB ERROR:", e)
        return False

def get_project(project_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name FROM subjects WHERE project_id = ?",
        (project_id,)
    )
    subjects = cursor.fetchall()

    result = []

    for s in subjects:
        subject_id, subject_name = s

        cursor.execute(
            "SELECT id, stuff FROM notes WHERE subject_id = ?",
            (subject_id,)
        )
        notes = cursor.fetchall()

        notes_list = [
            {"note_id": n[0], "stuff": n[1]} for n in notes
        ]

        result.append({
            "subject_id": subject_id,
            "subject_name": subject_name,
            "notes": notes_list
        })

    conn.close()
    return result

def addsubject(name, project_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO subjects (name, project_id) VALUES (?, ?)",
        (name, project_id)
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except Exception as e:
        print("DB ERROR:", e)
        return None

def addnote(subject_id, stuff):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO notes (subject_id, stuff) VALUES (?, ?)",
        (subject_id, stuff)
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except Exception as e:
        print("DB ERROR:", e)
        return None
    
def updatesubject(new_name, id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE subjects SET name = ? WHERE id = ?",
        (new_name, id)               
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no subject was updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False
    
def updatenote(newstuff, note_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE notes SET stuff = ? WHERE id = ?",
        (newstuff, note_id)               
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no note updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False
    
def deletesubject(id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM subjects WHERE id = ?",
        (id,)
        )

        conn.commit()
        conn.close()
        return True
    except:
        return False
    
def deletenote(id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM notes WHERE id = ?",
        (id,)
        )

        conn.commit()
        conn.close()
        return True
    except:
        return False

def showall():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM subjects",)
    allsubjects = cursor.fetchall()

    result = []

    for thing in allsubjects:
        subject_id = thing[0]
        subject_name = thing[1]

        cursor.execute("SELECT id, stuff FROM notes WHERE subject_id = ?",
        (subject_id,)
        )
        allnotes = cursor.fetchall()

        if allnotes:
            noteslist = [{"note_id": n[0], "stuff": n[1]} for n in allnotes]
        else:
            noteslist = []

        result.append({
            "subject_id": subject_id,
            "subject_name": subject_name,
            "notes": noteslist
        })

    conn.close()
    return result

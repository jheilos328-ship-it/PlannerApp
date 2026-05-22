import sqlite3
import os

def connect():
    db_path = os.environ.get("PLANNER_DB_PATH")
    if not db_path:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "v4schoolway2clean.db")

    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    print("Using DB:", db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def ensure_column(table, column, definition):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        conn.commit()

    conn.close()

def create_subject_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_id INTEGER,
            due_date TEXT,
            priority TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    ensure_column("subjects", "due_date", "TEXT")
    ensure_column("subjects", "priority", "TEXT")

def create_notes_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        stuff TEXT NOT NULL,
        due_date TEXT,
        priority TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE        
        )
    """)
        
    conn.commit()
    conn.close()
    ensure_column("notes", "due_date", "TEXT")
    ensure_column("notes", "priority", "TEXT")

def create_projects_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT,
            priority TEXT
        )
    """)

    conn.commit()
    conn.close()
    ensure_column("projects", "due_date", "TEXT")
    ensure_column("projects", "priority", "TEXT")

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

def updateproject(new_name, project_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE projects SET name = ? WHERE id = ?",
            (new_name, project_id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no project was updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False

def updateprojectdate(due_date, project_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE projects SET due_date = ? WHERE id = ?",
            (due_date, project_id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no project due date was updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False

def updateprojectpriority(priority, project_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE projects SET priority = ? WHERE id = ?",
            (priority, project_id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no project priority was updated.")
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

        cursor.execute("SELECT id, name, due_date, priority FROM projects")
        allprojects = cursor.fetchall()

        result = []
        for p in allprojects:
            project_id = p[0]
            project_name = p[1]
            due_date = p[2]
            priority = p[3]

            result.append({
                "project_id": project_id,
                "project_name": project_name,
                "due_date": due_date,
                "priority": priority
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
        "SELECT id, name, due_date, priority FROM subjects WHERE project_id = ?",
        (project_id,)
    )
    subjects = cursor.fetchall()

    result = []

    for s in subjects:
        subject_id, subject_name, subject_due_date, subject_priority = s

        cursor.execute(
            "SELECT id, stuff, due_date, priority FROM notes WHERE subject_id = ?",
            (subject_id,)
        )
        notes = cursor.fetchall()

        notes_list = [
            {"note_id": n[0], "stuff": n[1], "due_date": n[2], "priority": n[3]} for n in notes
        ]

        result.append({
            "subject_id": subject_id,
            "subject_name": subject_name,
            "due_date": subject_due_date,
            "priority": subject_priority,
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

def updatesubjectdate(due_date, id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE subjects SET due_date = ? WHERE id = ?",
        (due_date, id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no subject due date was updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False

def updatesubjectpriority(priority, id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE subjects SET priority = ? WHERE id = ?",
        (priority, id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no subject priority was updated.")
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

def updatenotedate(due_date, note_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE notes SET due_date = ? WHERE id = ?",
        (due_date, note_id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no note due date was updated.")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False

def updatenotepriority(priority, note_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("UPDATE notes SET priority = ? WHERE id = ?",
        (priority, note_id)
        )

        conn.commit()
        if cursor.rowcount == 0:
            print("no note priority was updated.")
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

    cursor.execute("SELECT id, name, due_date, priority FROM subjects",)
    allsubjects = cursor.fetchall()

    result = []

    for thing in allsubjects:
        subject_id = thing[0]
        subject_name = thing[1]
        subject_due_date = thing[2]
        subject_priority = thing[3]

        cursor.execute("SELECT id, stuff, due_date, priority FROM notes WHERE subject_id = ?",
        (subject_id,)
        )
        allnotes = cursor.fetchall()

        if allnotes:
            noteslist = [{"note_id": n[0], "stuff": n[1], "due_date": n[2], "priority": n[3]} for n in allnotes]
        else:
            noteslist = []

        result.append({
            "subject_id": subject_id,
            "subject_name": subject_name,
            "due_date": subject_due_date,
            "priority": subject_priority,
            "notes": noteslist
        })

    conn.close()
    return result

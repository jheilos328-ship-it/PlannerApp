from dataway2clean import create_subject_table, create_notes_table, create_projects_table, create_project, deleteproject, updateproject, updateprojectdate, updateprojectpriority, get_project, addsubject, addnote, updatesubject, updatesubjectdate, updatesubjectpriority, updatenote, updatenotedate, updatenotepriority, deletesubject, deletenote, showall, show_all_projects
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"],
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

create_projects_table()
create_subject_table()
create_notes_table()

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(BASE_DIR, "clientway2clean.html")

@app.route("/createnewproject", methods=["POST"])
def createproject():
    data = request.json
    name = data.get("name")

    project_id = create_project(name)

    if project_id:
        return jsonify({"project_id": project_id, "name": name})
    return jsonify({"message": "error!"})

@app.route("/getaproject", methods=["POST"])
def getproject():
    data = request.json
    project_id = data.get("project_id")

    action = get_project(project_id)

    if action is not None:
        return jsonify(action)
    return jsonify({"message": "error!"})

@app.route("/showallprojects", methods=["GET"])
def show_allprojects():
    everyproject = show_all_projects()
    return jsonify(everyproject)

@app.route("/updateproject", methods=["PATCH"])
def update_project():
    data = request.json
    project_id = data.get("project_id")
    new_name = data.get("new_name")

    action = updateproject(new_name, project_id)

    if action:
        return jsonify({"message": "updated!"})
    return jsonify({"message": "error!"})

@app.route("/updateprojectdate", methods=["PATCH"])
def update_project_date():
    data = request.json
    project_id = data.get("project_id")
    due_date = data.get("due_date")

    action = updateprojectdate(due_date, project_id)

    if action:
        return jsonify({"message": "updated!", "due_date": due_date})
    return jsonify({"message": "error!"})

@app.route("/updateprojectpriority", methods=["PATCH"])
def update_project_priority():
    data = request.json
    project_id = data.get("project_id")
    priority = data.get("priority")

    action = updateprojectpriority(priority, project_id)

    if action:
        return jsonify({"message": "updated!", "priority": priority})
    return jsonify({"message": "error!"})

@app.route("/addsubject", methods=["POST"])
def add_subject():
    data = request.json
    name = data.get("name")
    project_id = data.get("project_id")

    new_id = addsubject(name, project_id)

    if new_id:
        return jsonify({"subject_id": new_id, "name": name})
    return jsonify({"message": "error!"})

@app.route("/addnote", methods=["POST"])
def add_note():
    data = request.json
    subject_id = data.get("subject_id")
    stuff = data.get("stuff")

    new_id = addnote(subject_id, stuff)

    if new_id:
        return jsonify({"note_id": new_id, "stuff": stuff})
    return jsonify({"message": "error!"})

@app.route("/updatesubject", methods=["PATCH"])
def update_sub():
    data = request.json
    id = data.get("id")
    new_name = data.get("new_name")

    action = updatesubject(new_name, id)

    if action:
        return jsonify({"message": "updated!"})
    return jsonify({"message": "error!"})

@app.route("/updatesubjectdate", methods=["PATCH"])
def update_subject_date():
    data = request.json
    id = data.get("id")
    due_date = data.get("due_date")

    action = updatesubjectdate(due_date, id)

    if action:
        return jsonify({"message": "updated!", "due_date": due_date})
    return jsonify({"message": "error!"})

@app.route("/updatesubjectpriority", methods=["PATCH"])
def update_subject_priority():
    data = request.json
    id = data.get("id")
    priority = data.get("priority")

    action = updatesubjectpriority(priority, id)

    if action:
        return jsonify({"message": "updated!", "priority": priority})
    return jsonify({"message": "error!"})

@app.route("/updatethenote", methods=["PATCH"])
def update_note():
    data = request.json
    note_id = data.get("note_id")
    newstuff = data.get("stuff")

    action = updatenote(newstuff, note_id)

    if action:
        return jsonify({"message": "updated!"})
    return jsonify({"message": "error!"})

@app.route("/updatenotedate", methods=["PATCH"])
def update_note_date():
    data = request.json
    note_id = data.get("note_id")
    due_date = data.get("due_date")

    action = updatenotedate(due_date, note_id)

    if action:
        return jsonify({"message": "updated!", "due_date": due_date})
    return jsonify({"message": "error!"})

@app.route("/updatenotepriority", methods=["PATCH"])
def update_note_priority():
    data = request.json
    note_id = data.get("note_id")
    priority = data.get("priority")

    action = updatenotepriority(priority, note_id)

    if action:
        return jsonify({"message": "updated!", "priority": priority})
    return jsonify({"message": "error!"})

@app.route("/showall", methods=["GET"])
def show_all():
    print("got to endpoint!")
    everything = showall()
    print("identifying show all, going to attempt to return everything!")
    return jsonify(everything)

@app.route("/delete_subject", methods=["DELETE"])
def delsubject():
    data = request.json
    id = data.get("id")

    action = deletesubject(id)
    if action:
        return jsonify({"message": "deleted_subject"})
    return jsonify({"message": "error!"})

@app.route("/delete_project", methods=["DELETE"])
def delproject():
    data = request.json
    project_id = data.get("project_id")

    action = deleteproject(project_id)
    if action:
        return jsonify({"message": "deleted_project"})
    return jsonify({"message": "error!"})

@app.route("/delete_note", methods=["DELETE"])
def delnote():
    data = request.json
    note_id = data.get("note_id")

    action = deletenote(note_id)
    if action:
        return jsonify({"message": "deleted_note"})
    return jsonify({"message": "error!"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
        use_reloader=False
    )

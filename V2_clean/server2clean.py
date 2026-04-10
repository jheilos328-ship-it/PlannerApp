from data2clean import create_subject_table, create_notes_table, create_projects_table, create_project, get_project, addsubject, addnote, updatesubject, updatenote, deletesubject, deletenote, showall, show_all_projects
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"],
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])

create_projects_table()
create_subject_table()
create_notes_table()

@app.route("/createnewproject", methods=["POST"])
def createproject():
    data = request.json
    name = data.get("name")

    action = create_project(name)

    if action:
        return jsonify({"message": "posted!"})
    return jsonify({"message": "error!"})

@app.route("/getaproject", methods=["GET"])
def getproject():
    data = request.json
    project_id = data.get("project_id")

    action = get_project(project_id)

    if action:
        return jsonify(action)
    return jsonify({"message": "error!"})

@app.route("/showallprojects", methods=["GET"])
def show_allprojects():
    everyproject = show_all_projects()
    return jsonify(everyproject)

@app.route("/addsubject", methods=["POST"])
def add_subject():
    data = request.json
    name = data.get("name")
    project_id = data.get("project_id")

    action = addsubject(name, project_id)

    if action:
        return jsonify({"message": "posted!"})
    return jsonify({"message": "error!"})

@app.route("/addnote", methods=["POST"])
def add_note():
    data = request.json
    subject_id = data.get("subject_id")
    stuff = data.get("stuff")

    action = addnote(subject_id, stuff)

    if action:
        return jsonify({"message": "posted!"})
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

@app.route("/updatethenote", methods=["PATCH"])
def update_note():
    data = request.json
    note_id = data.get("note_id")
    newstuff = data.get("stuff")

    action = updatenote(newstuff, note_id)

    if action:
        return jsonify({"message": "updated!"})
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

@app.route("/delete_note", methods=["DELETE"])
def delnote():
    data = request.json
    note_id = data.get("note_id")

    action = deletenote(note_id)
    if action:
        return jsonify({"message": "deleted_note"})
    return jsonify({"message": "error!"})

if __name__ == "__main__":
    app.run(debug=True)
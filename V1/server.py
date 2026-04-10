from V1.database import add_subject_and_notes, add_subject, add_notes, show_all, create_table
from flask import Flask, jsonify, request

app = Flask(__name__)

create_table()

@app.route("/addsubjectandnotes", methods=["POST"])
def addall():
    data = request.json
    subject = data.get("subjectname")
    notes = data.get("thenotes")

    #temporary debug
    print("recieved:", subject, notes)

    happened = add_subject_and_notes(subject, notes)

    if happened:
        return jsonify({"message": "success!"}), 201
    return jsonify({"message": "could not post."}), 500 #THIS WORKS

@app.route("/addsubject", methods=["POST"])
def addsubject():
    data = request.json
    subject = data.get("subjectname")

    happened = add_subject(subject)

    if happened:
        return jsonify({"message": "success!"}), 201
    return jsonify({"message": "could not post."}), 500 #THIS ALSO WORKS

@app.route("/addnotes", methods=["POST"])
def addnotes():
    notes = request.json.get("thenotes")

    happened = add_notes(notes)

    if happened:
        return jsonify({"message": "success!"}), 201
    return jsonify({"message": "could not post."}), 500 

@app.route("/showeverything", methods=["GET"])
def show():
    happened = show_all()

    if happened:
        return jsonify({"subjects": happened}), 200
    return jsonify({"message": "could not show."}), 500

if __name__ == "__main__":
    app.run(debug=True)


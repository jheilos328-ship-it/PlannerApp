from database2 import create_subject_table, create_notes_table, add_subject, get_subject_id, add_notes, get_note_id, update_subject_name, update_notes, get_subject, get_notes, get_subject_and_notes, delete_subject, delete_note
from flask import Flask, jsonify, request

app = Flask(__name__)

create_subject_table()
create_notes_table()

data = request.json

@app.route("/add_subject", methods=["POST"])
def addsubject():
    subject = data.get("subject")

    add_subject(subject)

@app.route("/getsubjectid", methods=["GET"])   #I need to refer to the paper i have on this.
def getsubjectid():
    name = data.get("name")

    get_subject_id(name)

@app.route("/addnotes", methods=["POST"])   #IDK if the database function for this is right
def addnotes():
    subject_id = data.get("subject_id")
    stuff = data.get("stuff")

    add_notes(subject_id, stuff)

@app.route("/getnoteid", methods=["GET"])   #IDK IF THIS IS EVEN NEEDED
def getnoteid():
    note_id = data.get("note_id")

    get_note_id()

@app.route("/updatesubjectname", methods=["UPDATE"])
def updatesubjectname():
    id = data.get("id")
    newname = data.get("newname")

    update_subject_name(newname, id)

@app.route("/updatenotes", methods=["UPDATE"])
def updatenote():
    note_id = data.get("noteid")
    newnote = data.get("newnotes")

    update_notes(newnote, note_id)

#GET SUBJECT
#GET NOTES

@app.route("/getsubjectandnotes", method=["GET"])
def getsubjectandnotes():
    subjectid = data.get("subjectid")

    get_subject_and_notes(subjectid)

@app.route("/deletesubject", methods=["DELETE"])
def deletesubject():
    



    
import json, requests
link = ""

def didrequestwork(response):
        print("status code", response.status_code)
        try:
            print(json.dumps(response.json(), indent=4))
        except Exception as e:
            print("couldnt parse json:", response.text)

print("add subject and notes? if none, type (n). note: you need to specify which subject if only adding notes")
print("type, (S)ee all in the subject name to see all")
def ask():
    subjectname = input("subject name?").lower().strip()

    if subjectname == "s":
        print("about to go to endpoint")
        endpoint = "/showeverything"
        print("did it work?")

    thenotes = input("notes?").lower().strip()

    if subjectname == "n":
        subjectname = None
    if thenotes == "n":
        thenotes = None

    if subjectname is None and thenotes is None:
        print("nothing happened.")
        return
    
    if subjectname is None:
        print("cant put the notes anywhere")
        return
    
    data = {"subjectname": subjectname, "thenotes": thenotes}
    
    if thenotes is None:
        endpoint = "/addsubject"
    
    else:
        endpoint = "/addsubjectandnotes"

    response = requests.post(f"{link}{endpoint}", json=data)
    didrequestwork(response)

ask()
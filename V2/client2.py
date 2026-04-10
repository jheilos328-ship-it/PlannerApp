import json, requests
link = ""

def didrequestwork(response):
        print("status code", response.status_code)
        try:
            print(json.dumps(response.json(), indent=4))
        except Exception as e:
            print("couldnt parse json:", response.text)

def ask():
    question = input("S+N = 'sn', S = 's', N = 'n', show all = 'all', none = 'no'")
    if question == "no":
        print("nothing happened.")
        return
    
    elif question == "s":
        print("sending to enpoint...")
        endpoint = ""
        print("sent!")

    elif question == "n":
        print("sending to endpoint...")
        endpoint = ""
        print("sent!")
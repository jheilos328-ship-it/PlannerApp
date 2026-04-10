import json, requests
link = "http://127.0.0.1:5000"

def ask():
    option = input("add (S), add (N), or show (A)ll?")
    if option == "S":
        endpoint = "/addsubject"
        name = input("name?")

        data = {"name": name}
        response = requests.post(f"{link}{endpoint}", json=data)
        print(json.dumps(response.json(), indent=4))

    elif option == "A":
        endpoint = "/showall"
        print("got the endpoint!")

        response = requests.get(f"{link}{endpoint}")
        print("Sent!")
        print(json.dumps(response.json(), indent=4))



ask()

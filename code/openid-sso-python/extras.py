import json

def print_json(stuff):
    a = json.dumps(stuff, indent=4)
    print(a)
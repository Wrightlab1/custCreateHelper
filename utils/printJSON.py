import json

# function to print json data in a more readable way


def printJSON(data):
    try:
        parsed = json.loads(data)
        print(json.dumps(parsed, indent=4))
    except ValueError as e:
        print(data)

import json

file = open("testjson.json")
d = json.load(file)
previousItem = 0.0
for key, value in d.items():
    print(key, str(value - previousItem))
    previousItem = value

import json


with open("obd_codes.json", "r") as f:
    data = json.load(f)

print(data)
import json

with open('accuracy/result.json', 'r') as fp:
    data = json.load(fp)


print(data)
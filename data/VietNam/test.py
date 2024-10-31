import json


with open("vocab.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("vocab.txt", "w", encoding="utf-8") as f:
    for key, value in data.items():
        f.write(key + "\n")

print('done')


import csv
import json

out = []
with open("src/features.csv", "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        row["default_value"] = float(row["default_value"])
        out.append(row)

with open("src/features.json", "w") as outfile:
    json.dump(out, outfile)


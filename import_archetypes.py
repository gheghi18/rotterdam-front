import csv
import json
import glob
import os

out = []

for f in glob.glob("archetypes/*.csv"):
    name = os.path.basename(f).replace(".csv", "")
    with open(f, "r") as infile:
        reader = csv.DictReader(infile)
        row = next(reader)
        for k in row:
            row[k] = float(row[k])

        item = {"name": name, "values": row}
        out.append(item)


with open("src/archetypes.json", "w") as outfile:
    json.dump(out, outfile)

import csv
import json

out = []
with open("../predict-api/src/sample.csv", "r") as infile:
    reader = csv.DictReader(infile)
    sample_rows = [r for r in reader]

sample_row = sample_rows[0]

with open("src/features.csv", "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        # row["default_value"] = float(row["default_value"])
        column = row["feature_dutch_underscore"]
        try:
            row["default_value"] = float(sample_row[column])
        except Exception as e:
            print(e)
            row["default_value"] = float(row["default_value"])
        out.append(row)

with open("src/features.json", "w") as outfile:
    json.dump(out, outfile)

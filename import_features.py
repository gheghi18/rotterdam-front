import csv
import json

out = []
with open("../predict-api/src/sample.csv", "r") as infile:
    reader = csv.DictReader(infile)
    sample_rows = [r for r in reader]

sample_row = sample_rows[0]

# with open("features.csv", "r") as infile:
#     reader = csv.DictReader(infile)
#     for row in reader:
#         # row["default_value"] = float(row["default_value"])
#         column = row["feature_dutch_underscore"]
#         row["index"] = int(row["index"])
#         if row["feature_english"] != "":
#             row["feature_english_auto_translate"] = row["feature_english"]
#         try:
#             row["default_value"] = float(sample_row[column])
#         except Exception as e:
#             print(e)
#             row["default_value"] = float(row["default_value"])
#         out.append(row)


feature_types = {}
with open("features_types.csv", "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        feature_types[row["feature_names_model"]] = row["subtype"]

vals = []
out = []
with open("features.csv", "r") as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)
    headers = list(rows[0].keys()) + ["type"]
    for row in rows:
        row["default_value"] = float(row["default_value"])
        column = row["feature_dutch_underscore"]
        row["index"] = int(row["index"])
        if row["feature_english"] != "":
            row["feature_english_auto_translate"] = row["feature_english"]
        # try:
        #     row["default_value"] = float(sample_row[column])
        # except Exception as e:
        #     print(e)
        #     row["default_value"] = float(row["default_value"])
        row["type"] = feature_types[row["feature_dutch_underscore"]]
        vals.append(list(row.values()))

# print(headers)
# print(vals[0])
with open("src/features.json", "w") as outfile:
    json.dump({"headers": headers, "values": vals}, outfile)

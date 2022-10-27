import csv

with open("../predict-api/src/sample.csv", "r") as infile:
    reader = csv.DictReader(infile)

    sample_headers = list(reader.fieldnames)


with open("src/features.csv", "r") as infile:
    reader = csv.DictReader(infile)
    new_headers = [r["feature_dutch_underscore"] for r in reader]


for h in sample_headers:
    if h not in new_headers:
        print(h)

for i,h in enumerate(sample_headers):
    # print(i+2, h)
    if h != new_headers[i]:
        print(i, h, new_headers[i])
#
print(len(new_headers), len(sample_headers))
for i,h in enumerate(new_headers):
    if h != sample_headers[i]:
        print(i, h, sample_headers[i])


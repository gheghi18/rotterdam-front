import csv
import json
import glob
import re

indices = {}


def get_indices():

    with open("key.txt", "r") as infile:
        key = infile.readlines()

    key = [l.strip() for l in key]

    with open("src/features.csv", "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            original_index = key.index(row["feature_dutch_underscore"])
            new_index = int(row["index"])
            indices[original_index] = new_index


def get_tree(filename):
    tree = []
    with open(filename, "r") as infile:
        rows = csv.reader(infile)
        next(rows)
        for r in rows:
            t_id, var_id, split, left, right = r
            t_id = int(t_id) - 1
            var_id = int(var_id)
            if var_id > -1:
                var_id = indices[int(var_id)]
            split = float(split)
            left = int(left)
            right = int(right)
            tree.append([t_id, var_id, split, left, right])
    return tree


def get_all_trees(folder="../visualize_trees/trees"):
    trees = []
    for f in glob.glob(folder + "/*.csv"):
        t = get_tree(f)
        tree_num = re.sub("\D", "", f)
        trees.append((tree_num, t))
    trees = sorted(trees, key=lambda t: t[0])
    trees = [t[1] for t in trees]
    return trees


get_indices()
keys = ["t_id", "var_id", "split", "left", "right"]
trees = get_all_trees()
with open("src/trees.json", "w") as outfile:
    json.dump({"keys": keys, "trees": trees}, outfile)

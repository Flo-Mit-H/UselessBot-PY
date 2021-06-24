import json
import os


def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(filename, contents):
    with open(filename, "w") as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)


def save_config():
    write_json("../config/config.json", config)


config = json.load(open(file="../config/config.json"))

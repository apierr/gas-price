#utility.py
import json, glob

def get_json_from_file(file_name):
    with open(file_name) as file:
        try:
            return json.load(file)
        except:
            return False

def get_files(pattern):
    return glob.glob(pattern)

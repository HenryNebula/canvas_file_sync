import json
from os import path
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--config", help="relative path for config file, the default is config.json", default="config.json")
parser.add_argument("--key", type=str, choices=["python", "base_path", "dest_path", "rclone"],
                    help="the value of which key to extract from" )
args = parser.parse_args()

key = args.key
config = args.config
file_path = path.dirname(path.abspath(__file__))
file_path = path.join(file_path, config)

with open(file_path) as f:
    dict_ = json.loads(f.read())

print(dict_[key])
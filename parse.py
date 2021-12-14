#! /usr/bin/python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "filename", help="Input request file. \t ex: ./burptopy req.txt ", type=str)
args = parser.parse_args()
print(args.filename)

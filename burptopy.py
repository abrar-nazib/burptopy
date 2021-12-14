#! /usr/bin/python3
import requests
import re
import argparse

# Getting the request file from user
parser = argparse.ArgumentParser()
parser.add_argument(
    "filepath", help="Input request file or file's path. \t ex: ./burptopy req.txt ", type=str)
args = parser.parse_args()
filepath = args.filepath


def parse_file(filepath):
    """ 
    Parse data from request file.
    Returns url, method, data, headers in a list.
    """

    # Gathering contents of request files into a list
    with open(filepath, 'r') as f:
        request_lines = f.readlines()

    # Determine Request method and take action accordingly
    method = determine_method(request_lines)
    # Parse the headers
    headers = parse_headers(request_lines, method)
    # Parse data and url
    data, schema, subdirectory = parse_data_and_url(request_lines, method)
    url = schema + headers["Host"] + subdirectory

    return [
        url,
        method,
        data,
        headers,
    ]


def determine_method(request_lines):
    """
    Regex for determining the request method
    """
    firstline = request_lines[0]
    firstline_regex = re.compile(r'^(\w+)')
    firstline_matches = firstline_regex.finditer(firstline)
    for firstline_match in firstline_matches:
        method = firstline_match.group(1)
    return method


def parse_headers(request_lines, method):

    # Parsing headers for post request
    headers = {}
    header_pattern = re.compile(r'(^[\w-]+):\s(.+)')
    x = None
    if(method == "POST"):
        x = -2
    elif(method == "GET"):
        x = None
    for line in request_lines[1:x]:
        header_matches = header_pattern.finditer(line)
        for header_match in header_matches:
            headers[header_match.group(1)] = header_match.group(2)
    return headers


def parse_data_and_url(request_lines, method):
    """
    Parses data and parameters and gets schema and subdirectory ready for parsing url
    """
    data = {}
    firstline = request_lines[0]
    firstline_regex = re.compile(r'^\w+\s(\S+)\s(.+)\n')
    firstline_matches = firstline_regex.finditer(firstline)
    for firstline_match in firstline_matches:
        subdirectory = firstline_match.group(1)
        if(firstline_match.group(2) == "HTTP/1.1"):
            schema = "https://"
        else:
            schema = "http://"
    if(method == "POST"):
        data_line = request_lines[-1]
        data = get_data(data_line)
    elif(method == "GET"):
        data_line = subdirectory
        # For separating subdirectory from parameters
        data_pattern = re.compile(r'(.+)\?(\S+)')
        data_matches = data_pattern.finditer(data_line)
        for data_match in data_matches:
            subdirectory = data_match.group(1)
            data_line = data_match.group(2)  # Group 2 contains paameters
            data = get_data(data_line)
    return [
        data,
        schema,
        subdirectory
    ]


def get_data(data_line):
    """
    For getting the regex done for parsing data
    """
    data = {}
    data_pattern = re.compile(r'&?((\w+)=(\w+))&?')
    data_matches = data_pattern.finditer(data_line)
    for data_match in data_matches:
        data[data_match.group(2)] = data_match.group(3)
    return data


url, method, data, headers = parse_file(filepath)
print("URL:")
print(url)
print("Request Method:")
print(method)
print("Data or Parameters:")
print(data)
print("Headers:")
print(headers)

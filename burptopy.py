#! /usr/bin/python3
from os import path
import requests
import re
import argparse         # For parsing user input
from urllib.parse import urlparse   # For parsing urls
from urllib.parse import parse_qs   # For parsing values

# Getting the request file from user
parser = argparse.ArgumentParser()
parser.add_argument(
    "filepath", help="Input request file or file's path. \t ex: ./burptopy req.txt ", type=str)
args = parser.parse_args()
filepath = args.filepath


class Burptopy:

    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self):
        """ 
        Parse data from request file.
        Returns url, method, data, headers in a list.
        """
        filepath = self.filepath
        # Gathering contents of request files into a list
        with open(filepath, 'r') as f:
            request_lines = f.readlines()

        # Determine Request method and take action accordingly
        method = self.determine_method(request_lines)
        # Parse the headers
        headers = self.parse_headers(request_lines, method)
        # Parse data and url
        data, schema, path = self.parse_data_and_url(request_lines, method)
        url = schema + headers["Host"] + path

        return [
            url,
            method,
            data,
            headers,
        ]

    @staticmethod
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

    @staticmethod
    def parse_headers(request_lines, method):

        # Parsing headers for post request
        headers = {}
        header_pattern = re.compile(r'(^[\w-]+):\s(.+)')

        x = -2 if (method == "POST") else None

        for line in request_lines[1:x]:
            header_matches = header_pattern.finditer(line)
            for header_match in header_matches:
                headers[header_match.group(1)] = header_match.group(2)
        if "Content-Length" in headers:
            headers.pop("Content-Length")
        return headers

    def parse_data_and_url(self, request_lines, method):
        """
        Parses data and parameters and gets schema and path ready for parsing url
        """
        data = {}
        firstline = request_lines[0]
        firstline_regex = re.compile(r'^\w+\s(\S+)\s(.+)\n')
        firstline_matches = firstline_regex.finditer(firstline)
        for firstline_match in firstline_matches:
            path = firstline_match.group(1)
            if(firstline_match.group(2) == "HTTP/1.1"):
                schema = "https://"
            else:
                schema = "http://"
        if(method == "POST"):
            data_line = request_lines[-1]
            data = self.get_data(data_line.strip())
        elif(method == "GET"):
            # for get request, path holds the url and params
            parsed_url = urlparse(path)
            path = parsed_url.path
            data = self.get_data(parsed_url.query)
        return [
            data,
            schema,
            path
        ]

    @staticmethod
    def get_data(data_line):
        """
        For getting the regex done for parsing data
        """
        data = {}
        data_results = parse_qs(data_line)
        for data_result in data_results:
            data[data_result] = data_results[data_result][0]
        return data


# burptopy_parser = Burptopy(filepath)
# url, method, data, headers = burptopy_parser.parse_file()
# print("URL:")
# print(url)
# print("Request Method:")
# print(method)
# print("Data or Parameters:")
# print(data)
# print("Headers:")
# print(headers)

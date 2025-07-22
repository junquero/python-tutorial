#!/usr/local/bin/python3.10

# This script is used to search and replace in files
# It uses the SearchAndReplace.py module to do the actual search and replace
# It is a wrapper script that allows for easy use of the SearchAndReplace.py module
# It is a shell script that can be used to search and replace in files
from SearchAndReplace import SearchAndReplace
import sys
import argparse
import logging.config


# Print usage and exit
def print_usage_and_exit(message):
    print(f"Error: {message}")
    parser.print_help()
    sys.exit(1)

# Check all arguments are present and print usage if not
def check_args(args : argparse.Namespace):
    if args.path is None:
        print_usage_and_exit("Path is required")
    if args.filter_string is None:
        print_usage_and_exit("Filter string is required")
    if args.search_regex is None:
        print_usage_and_exit("Search regex is required")
    if args.replace_string is None:
        print_usage_and_exit("Replace string is required")

# Use argparse to parse the arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Search and replace in files')
    parser.add_argument('-p', '--path', type=str, help='The path to the files to search and replace in')
    parser.add_argument('-f', '--filter_string', type=str, help='The filter to use to select the files to search and replace in')
    parser.add_argument('-s', '--search_regex', type=str, help='The regex to search for')
    parser.add_argument('-r', '--replace_string', type=str, help='The string to replace the search_regex with')
    parser.add_argument('-b', '--backup', action='store_true', help='Backup the original files with extension .bak')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    return parser.parse_args()

def main():
    logging.config.fileConfig('logging.conf')

    args = parse_args()
    check_args(args)

    search_and_replace = SearchAndReplace(args.verbose)
    search_and_replace.search_and_replace_in_files(args.path, args.filter_string, args.search_regex, args.replace_string, args.backup)

if __name__ == "__main__":
    main()

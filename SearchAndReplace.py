# List files in the current directory
import os
import re
import logging

# Class to search and replace in files
class SearchAndReplace:
    def __init__(self):
        # Add a logger
        self.logger = logging.getLogger(__name__)

    # Get files in the directory path and subdirectories recursively, returning the list of files
    # Parameters:
    # path: string, the path to the directory to search in recursively.
    # filter_regex_string: string, the regex to filter the files to search in. If None, all files will be searched.
    # Returns: list of strings, the list of files in the directory path and subdirectories. The file names are relative to the path.
    # For example, if the path is "documents" and the filter_regex_string is ".*\\.doc$", the 
    # function will return a list of strings like ["documents\file1.doc", "documents\subdir\file2.doc"]
    def get_all_files_in_path_matching_regex(self, path, filter_regex_string=None):
        files_list = []
        if filter_regex_string is None:
            filter_regex = None
        else:
            filter_regex = re.compile(filter_regex_string)

        for root, dirs, files in os.walk(path):
            for file in files:
                if filter_regex is None or filter_regex.match(file):
                    files_list.append(os.path.join(root, file))
        return files_list

    # Convert traditional star filter into regex
    def convert_star_filter_to_regex(self, filter_string):
        if filter_string is None:
            return None
        return filter_string.replace(".","\\.").replace("*", ".*")+"$"

    # The filter is in the usual *.txt format. The filter string is converted to a regex.
    def get_all_files_in_path_matching_filter(self, path, filter_string):
        filter_regex = self.convert_star_filter_to_regex(filter_string)
        return self.get_all_files_in_path_matching_regex(path, filter_regex)

    # Description: Search and replace in files in a directory matching a regex including subdirectories
    # It creates a backup of the original file before replacing the content with extension .bak. If a file exists with the same name as the backup, it will be overwritten. 
    # Parameters:
    # path: string, the path to the directory to search in recursively.
    # filter_string: string, the star filter to filter the files to search in. If None, all files will be searched.
    # search_regex_string: string, the regex to search for.
    # replace_string: string, the string to replace the search string with
    # Returns: None
    def search_and_replace_in_files(self, path, filter_string, search_regex_string, replace_string):
        search_regex = re.compile(search_regex_string)
        files_list = self.get_all_files_in_path_matching_filter(path, filter_string)
        for file in files_list:
            with open(file, "r") as f:
                content = f.read()
            
            new_content = re.sub(search_regex, replace_string, content)
            self.logger.debug(f"Processing {file} for filter {filter_string}")

            if new_content != content:
                self.logger.debug(f"Replacing {search_regex_string} with {replace_string} in {file}")
                with open(file+".bak", "w") as f:
                    f.write(content)
                with open(file, "w") as f:
                    f.write(new_content)
    
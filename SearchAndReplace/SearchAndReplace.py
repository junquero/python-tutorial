# List files in the current directory
import fnmatch
import os
import re
import logging
import logging.config

# Class to search and replace in files
class SearchAndReplace:
    def __init__(self, verbose=False):
        # Add a logger
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose


    def matches_pattern(self, string, pattern):
        if not isinstance(pattern, str) or not pattern:
            return False
        if os.name == 'nt':
            return fnmatch.fnmatch(string, pattern)
        else:
            return fnmatch.fnmatchcase(string, pattern)

    # Get files in the directory path and subdirectories recursively, returning the list of files
    # Parameters:
    # path: string, the path to the directory to search in recursively.
    # filter_regex_string: string, the regex to filter the files to search in. If None, all files will be searched.
    # Returns: list of strings, the list of files in the directory path and subdirectories. The file names are relative to the path.
    # For example, if the path is "documents" and the filter_regex_string is ".*\\.doc$", the 
    # function will return a list of strings like ["documents\file1.doc", "documents\subdir\file2.doc"]
    def get_all_files_in_path_matching_pattern(self, path, pattern=None):
        if self.verbose:
            self.logger.info(f"Getting all files in path {path} matching pattern {pattern}")
        files_list = []
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if pattern is None or self.matches_pattern(file, pattern):
                    files_list.append(os.path.join(root, file))
        return files_list

    # The filter is in the usual *.txt format. The filter string is converted to a regex.
    def get_all_files_in_path_matching_filter(self, path, pattern):
        return self.get_all_files_in_path_matching_pattern(path, pattern)

    # Description: Search and replace in files in a directory matching a regex including subdirectories
    # It creates a backup of the original file before replacing the content with extension .bak. If a file exists with the same name as the backup, it will be overwritten. 
    # Parameters:
    # path: string, the path to the directory to search in recursively.
    # filter_string: string, the star filter to filter the files to search in. If None, all files will be searched.
    # search_regex_string: string, the regex to search for.
    # replace_string: string, the string to replace the search string with
    # Returns: None
    def search_and_replace_in_files(self, path, filter_string, search_regex_string, replace_string, backup_enabled=True):
        search_regex = re.compile(search_regex_string)
        files_list = self.get_all_files_in_path_matching_filter(path, filter_string)
        if self.verbose:
            self.logger.info(f"Found {len(files_list)} files matching filter {filter_string} to search and replace in")

        for file in files_list:
            with open(file, "r") as f:
                content = f.read()
            
            new_content = re.sub(search_regex, replace_string, content)
            if self.verbose:
                self.logger.info(f"Processing {file}. Search {search_regex_string} and replace with {replace_string}")

            if new_content != content:
                if self.verbose:
                    self.logger.info(f"Replacing {search_regex_string} with {replace_string} in {file}")
                if backup_enabled:
                    with open(file+".bak", "w") as f:
                        f.write(content)
                    if self.verbose:
                        self.logger.info(f"Backup file {file}.bak created")
                with open(file, "w") as f:
                    f.write(new_content)
            else:
                if self.verbose:
                    self.logger.info(f"Text not found in {file}")
# The name of the file must start with test_ to be run by unittest
# The class name must start with Test to be run by unittest
# The method name must start with test_ to be run by unittest   


from itertools import tee
from SearchAndReplace import SearchAndReplace
import os
import logging
import logging.config
import shutil
import unittest

logging.config.fileConfig('logging.conf')

class TestSearchAndReplace (unittest.TestCase):

    # This method is run before each test
    def setUp(self):
        self.search_and_replace = SearchAndReplace()

    def test_filter_single_file(self):
        files_list = self.search_and_replace.get_all_files_in_path_matching_filter(".", "Test1.txt")
        assert len(files_list) == 1, "Expected 1 file, got " + str(len(files_list))
        expected_path = os.path.join(".", "Test1.txt")
        assert files_list[0] == expected_path, f"Expected {expected_path}, got {files_list[0]}"

    def test_filter_txt_files(self):
        files_list = self.search_and_replace.get_all_files_in_path_matching_filter(".", "*.txt")
        assert len(files_list) == 3, "Expected 3 file, got " + str(len(files_list))

    def test_filter_single_file_regex(self):
        files_list = self.search_and_replace.get_all_files_in_path_matching_regex(".", "Test1\\.txt$")
        assert len(files_list) == 1, "Expected 1 file, got " + str(len(files_list))
        expected_path = os.path.join(".", "Test1.txt")
        assert files_list[0] == expected_path, f"Expected {expected_path}, got {files_list[0]}"

    def test_search_and_replace_in_files(self):
        self.search_and_replace.search_and_replace_in_files(".", "Test1.txt", "old", "new")
        # Assert that the replacement worked in Test1.txt
        with open("Test1.txt", "r") as f:
            content = f.read()
        assert "new test string" in content, "Replacement did not work in Test1.txt"
        # Assert that the backup file was created
        assert os.path.exists("Test1.txt.bak"), "Backup file was not created"
        # Assert that the backup file contains the original content
        with open("Test1.txt.bak", "r") as f:
            backup_content = f.read()
        assert "old test string" in backup_content, "Backup file does not contain the original content"
        # copy backup to original file to revert to initial state
        shutil.move("Test1.txt.bak", "Test1.txt")
        # assert backup file doesn't exist
        assert not os.path.exists("Test1.txt.bak"), "Backup file still exists"

    def test_search_and_replace_in_dual_files(self):
        self.search_and_replace.search_and_replace_in_files(".", "Test*.txt", "old", "new")
        # Assert that the replacement worked in Test1.txt and Test2.txt
        with open("Test1.txt", "r") as f:
            content = f.read()
        assert "new test string" in content, "Replacement did not work in Test1.txt"
        with open("Test2.txt", "r") as f:
            content = f.read()
        assert "test text" in content, "Replacement did not work in Test2.txt"
        # Assert that the backup file was created
        assert os.path.exists("Test1.txt.bak"), "Backup file was not created"
        assert not os.path.exists("Test2.txt.bak"), "Backup file was created"
        # Assert that the backup file contains the original content
        with open("Test1.txt.bak", "r") as f:
            backup_content = f.read()
        assert "old test string" in backup_content, "Backup file does not contain the original content"
        # copy backup to original file to revert to initial state
        shutil.move("Test1.txt.bak", "Test1.txt")
        # assert backup file doesn't exist
        assert not os.path.exists("Test1.txt.bak"), "Backup file still exists"

    def test_search_and_replace_with_unicode(self):
        self.search_and_replace.search_and_replace_in_files(".", "Test *.txt", "☘️", "✅")
        # Assert that the replacement worked in Test1.txt
        with open("Test Unicode.txt", "r") as f:
            content = f.read()
        assert "✅" in content, "Replacement did not work in Test Unicode.txt"
        # copy backup to original file to revert to initial state
        shutil.move("Test Unicode.txt.bak", "Test Unicode.txt")
        # assert backup file doesn't exist
        assert not os.path.exists("Test Unicodet1.txt.bak"), "Backup file still exists"

    def test_convert_star_filter_to_regex(self):
        assert self.search_and_replace.convert_star_filter_to_regex("*.txt") == ".*\\.txt$"
        assert self.search_and_replace.convert_star_filter_to_regex("*.doc") == ".*\\.doc$"
        assert self.search_and_replace.convert_star_filter_to_regex("*.docx") == ".*\\.docx$"
        assert self.search_and_replace.convert_star_filter_to_regex(".doc") == "\\.doc$"
        assert self.search_and_replace.convert_star_filter_to_regex("doc") == "doc$"

# Code to run the tests
if __name__ == '__main__':
    unittest.main()


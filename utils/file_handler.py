import os


"""
FileHandler
@desc:
    Should handle file operations like create, delete, search, read
"""


class FileHandler:

    def search(self, path, file_to_search):
        for root, dirs, files in os.walk(path):
            if file_to_search in files:
                return file_to_search

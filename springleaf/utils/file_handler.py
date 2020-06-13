import json
import os

from pkg_resources import resource_stream

import springleaf
import yaml


"""
FileHandler
@desc:
    Should handle file operations like create, delete, search, read
"""


class FileHandler:

    """
    search
    @desc:
        Searches for file with given path
    @params:
        path - path,
        file - file to search
        absolute [False] - returns full path of file
    @return: file_name - returns a file name if file is found
    """

    @staticmethod
    def search(path, file, absolute=False):
        for root, dirs, files in os.walk(path):
            if file in files:
                if absolute:
                    return os.path.join(root, file)
                return file

    """
    get_first_file_in_tree
    @desc:
        We are getting Main class, as it's in top package we can take it as first file found
    @return:  path -  Absolute path to the first file
    """
    @staticmethod
    def get_first_file_in_tree(path):
        first_file = False

        for root, dirs, files, in os.walk(path):
            for i in files:
                first_file = os.path.join(root, i)
                break
            if first_file:
                break
        return first_file

    @staticmethod
    def read_file(path):
        try:
            file = open(path)
            content = file.read()
            file.close()
            return content
        except TypeError:
            return None

    """
    current_dir
    @desc:
        Return path from current working directory
    @return:  string -  path
    """

    @staticmethod
    def current_dir():
        return os.path.abspath(os.getcwd())

    @staticmethod
    def script_dir():
        # We want to return path from springleaf script, but with this we get the path of file_handler.py
        # which is in /utils so we substring from end 5 chars
        return os.path.dirname(os.path.realpath(__file__))[:-5]
    """
    create_config_file
    @desc:
        Creates config file in which we can save project structure and future possible features
    @return: void -
    """

    @staticmethod
    def create_config_file(options_to_write: list):
        with open(FileHandler.current_dir() + "/springleaf.yaml", "w") as file:
            file.write("# SpringLeaf CLI - http://github.com/OMKE/SpringLeaf\n")
            config = yaml.dump(options_to_write, file, indent=4)

    @staticmethod
    def has_config_file():
        if FileHandler.search(FileHandler.current_dir(), "springleaf.yaml"):
            return True
        else:
            return False

    """
    get_project_structures
    @desc:
        Reads predefined project structures from ./common/project_structures.json
    @return: list - list od project structures
    """

    @staticmethod
    def get_project_structures():
        return FileHandler.get_src_file("project_structures.json")

    @staticmethod
    def get_project_structure(name):
        for i in FileHandler.get_project_structures():
            if i["name"] == name:
                return i

    @staticmethod
    def is_spring_dir():
        if FileHandler.is_executable(
                FileHandler.search(FileHandler.current_dir(), "gradlew", absolute=True)) or FileHandler.is_executable(
                FileHandler.search(FileHandler.current_dir(), "mvnw", absolute=True)):
            return True

        return False

    @staticmethod
    def is_executable(path):
        maven_meta = "#!/bin/sh"
        gradle_meta = "#!/usr/bin/env sh"
        file = FileHandler.read_file(path)
        if file:
            if file[0:9] == maven_meta or file[0:17] == gradle_meta:
                return True

        return False

    @staticmethod
    def is_maven(path=None):
        if path is None:
            path = FileHandler.current_dir() + "/mvnw"
        maven_meta = "#!/bin/sh"
        file = FileHandler.read_file(path)
        if file:
            if file[0:9] == maven_meta:
                return True
        return False

    @staticmethod
    def is_gradle(path=None):
        if path is None:
            path = FileHandler.current_dir() + "/gradlew"
        gradle_meta = "#!/usr/bin/env sh"
        file = FileHandler.read_file(path)
        if file:
            if file[0:17] == gradle_meta:
                return True

        return False

    @staticmethod
    def get_src_file(file_name, as_json=True):
        if as_json:
            return json.loads(resource_stream(springleaf.__name__, "common/" + file_name).read().decode())
        else:
            return resource_stream(springleaf.__name__, "common/" + file_name).read().decode()

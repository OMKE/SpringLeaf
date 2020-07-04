import json
import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from pkg_resources import resource_filename, resource_stream

import springleaf
import yaml
from springleaf.utils.exceptions import InvalidConfigFileException


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
    exits
    @desc:
        Check if file or folder exists on given path
    @return: bool - true if exists, else false
    """

    @staticmethod
    def exists(path):
        if os.path.isdir(path):
            return True
        if os.path.exists(path):
            return True
        return False

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
    get_model_name
    @desc:
        Looks for models in model folder and returns a list of founded
    @return: list - list of founded models
    """

    @staticmethod
    def get_model_names():
        # package name replaced dots with slashes so we get path like string
        package = FileHandler.get_from_config_file('package').replace(".", "/")
        model_folder_name = FileHandler.get_from_config_file(
            'entities-folder').replace(".", "/")  # folder that stores entities
        entities_path = "src/main/java/" + package + "/" + model_folder_name + "/"

        try:
            found_files = os.listdir(entities_path)
            return [file[:-5] for file in found_files if file[-5:] == ".java"]
        except:
            raise InvalidConfigFileException()

    """
    get_project_structures
    @desc:
        Reads predefined project structures from ./common/project_structures.json
    @return: list - list od project structures
    """

    @staticmethod
    def get_project_structures():
        return FileHandler.get_src_file("project_structures.json")

    """
    get_project_structure
    @desc:
        Looks in project_structures.json file and returns a value with given key
    @return: str - value of the key
    """

    @staticmethod
    def get_project_structure(name):
        for i in FileHandler.get_project_structures():
            if i["name"] == name:
                return i

    @staticmethod
    def get_project_structure_content(name):
        for i in FileHandler.get_project_structures():
            if i["name"] == name:
                return i["structure"]

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

    @staticmethod
    def get_template_file(file_name):
        return resource_stream(springleaf.__name__, "common/templates/" + file_name).read().decode()

    # @TODO - read gradle file
    """
    read_pom_file
    @desc:
        Reads pom file
    @return: dict - dict type
    """

    @staticmethod
    def read_pom_file():
        tree = ET.parse(FileHandler.current_dir() + "/pom.xml")
        root = tree.getroot()
        namesp = root.tag.replace("project", "")
        group_id = root.find(namesp+"groupId")
        name = root.find(namesp+"name")
        return {
            "groupId": group_id.text,
            "name": name.text
        }

    @staticmethod
    def get_from_config_file(key):
        with open(FileHandler.current_dir() + "/springleaf.yaml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            return config['springleaf']['project'][key]

    """
    validate_config_file
    @desc:
        Validates config file based on keys,
        @TODO - make a initial file in common, create and validate based on that file
    @return: bool - returns true if there are keys that we want, else false
    """

    @staticmethod
    def validate_config_file():
        is_valid = True
        config_attributes = ["build", 'name', 'package',
                             'structure', 'entities-folder', 'methods']
        with open(FileHandler.current_dir() + "/springleaf.yaml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            for i in config_attributes:
                if i not in config["springleaf"]["project"] or config['springleaf']['project'][i] == None:
                    is_valid = False
        return is_valid

    @staticmethod
    def create_folder_structure(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def unzip_file(extract_dir, file_name):
        file_path = resource_filename(
            springleaf.__name__, f"common/spring-build/{file_name}")
        with ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

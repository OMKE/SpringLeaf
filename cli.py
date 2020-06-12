
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

from PyInquirer import (Separator, Token, ValidationError, Validator, prompt,
                        style_from_dict)

from generator import Generator
from utils.file_handler import FileHandler
from utils.handlers.checkbox_handler import CheckBoxHandler
from utils.handlers.name_handler import NameHandler
# Handlers
from utils.handlers.project_structure_handler import ProjectStructureHandler
from utils.prompt_builder import PromptBuilder


"""
CLI
@desc:
    Main class
"""


class CLI:

    def __init__(self):
        self.generator = Generator()

        self.setup()

    def setup(self):
        # self.generator.generate()
        if(FileHandler.has_config_file()):
            # Do validaiton of config file
            pass
        else:
            self.ask_for_project_structure()

    """
    ask_for_project_structure
    @desc:
        Asks user to select project structure only if config file is not present in cwd
    @return: void - 
    """

    def ask_for_project_structure(self):
        prompt = PromptBuilder().create_question().set_type("list").set_message("Which project structure to use?").set_name("structure").set_choices(
            self.get_project_structure_names() + [Separator(), {"name": "Don't know which to use?", "disabled": "Check documentation for examples"}]).set_handler(
                ProjectStructureHandler)

        prompt.prompt(handle=True)

    def config_file_options(self, options: dict):

        return {
            "project_structure": options["project_structure"]
        }

    """
    get_project_structure_names
    @desc:
        Gets project structures, appends custom option and returns a list of names
    @return: list - names
    """

    def get_project_structure_names(self):
        names = []
        for i in self.get_project_structures():
            names.append(i["name"])

        names.append("Custom")
        return names

    """
    get_project_structures
    @desc:
        Returns dict of project structures
    @return: dict - dict of project structures
    """

    def get_project_structures(self):
        return FileHandler.get_project_structures()

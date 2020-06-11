
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

from PyInquirer import (Separator, Token, ValidationError, Validator, prompt,
                        style_from_dict)

from generator import Generator
from utils.file_handler import FileHandler
from utils.handlers.name_handler import NameHandler
# Handlers
from utils.handlers.project_structure_handler import ProjectStructureHandler
from utils.prompt_builder import PromptBuilder

"""
CLI
@desc:
    Main class
"""


style = style_from_dict({
    Token.Pointer: "#83E774"
})


class NameValidator(Validator):
    def validate(self, document):
        if len(document.text) < 3:
            raise ValidationError(
                message="Name can not be shorter than 3 chars",
                cursor_position=len(document.text)
            )


class CLI:

    def __init__(self):
        self.generator = Generator()

        self.setup()

    def setup(self):
        # self.generator.generate()
        if(FileHandler.has_config_file()):
            # Do validaiton
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
        prompt = PromptBuilder().add_type("list").add_message("Which project structure to use?").add_name("structure").add_choices(
            self.get_project_structure_names() + [Separator(), {"name": "Don't know which to use?", "disabled": "Check documentation for examples"}]).add_handler(
                ProjectStructureHandler).ask()
        prompt.handle()

        prompt = PromptBuilder().add_type("input").add_message(
            "What's your name?").add_name("name").add_handler(NameHandler).add_validator(NameValidator).ask()
        prompt.handle()

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

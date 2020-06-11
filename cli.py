
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

from PyInquirer import Separator, Token, prompt, style_from_dict

from generator import Generator
from utils.file_handler import FileHandler
from utils.prompt import Prompt

"""
CLI
@desc:
    Main class
"""


style = style_from_dict({
    Token.Pointer: "#83E774"
})


class CLI:

    def __init__(self):
        self.generator = Generator()

        self.setup()

    def setup(self):
        # self.generator.generate()
        FileHandler.create_config_file([])
        self.show_list()

    def show_list(self):
        self.ask_for_project_structure()

    """
    ask_for_project_structure
    @desc:
        Asks user to select project structure only if config file is not present in cwd
    @return: void - 
    """

    def ask_for_project_structure(self):
        prompt = Prompt()
        prompt.add_question("list", "Which project structure to use?", "structure",
                            self.get_project_structure_names() + [Separator(), {"name": "Don't know which to use?", "disabled": "Check documentation for examples"}])
        answers = prompt.ask()
        pprint(answers)

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

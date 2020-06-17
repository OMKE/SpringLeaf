
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

from pyfiglet import Figlet
from questionary import Separator
from rich.console import Console

import springleaf
from springleaf.generator import Generator
from springleaf.utils.file_handler import FileHandler
from springleaf.utils.handlers.checkbox_handler import CheckBoxHandler
from springleaf.utils.handlers.name_handler import NameHandler
# Handlers
from springleaf.utils.handlers.project_structure_handler import \
    ProjectStructureHandler

from .utils.prompt_builder import PromptBuilder


"""
CLI
@desc:
    Main class
"""


class CLI:

    WARNING = '\033[93m'

    def __init__(self, args):
        self.console = Console()
        self.args = args
        self.setup()

    def add_args(self):
        # self.arg_parser.add_argument(
        #     'new', 'n', type=str, help="Initialize a new Spring Starter Project")

        # return self.arg_parser.parse_args()
        pass

    def setup(self):
        # self.generator.generate()
        if(FileHandler.is_spring_dir()):
            if(FileHandler.has_config_file()):
                if FileHandler.validate_config_file():
                    # proceed to generate what users wants
                    pass
                else:
                    self.console.print("Invalid config file", style="red bold")
            else:
                self.ask_for_project_structure()
        else:
            self.console.print("Not a Spring Boot project", style="red bold")
            self.console.print(
                "Create new project with \n$ springleaf new <name>", style="yellow bold")

    """
    ask_for_project_structure
    @desc:
        Asks user to select project structure only if config file is not present in cwd
    @return: void - 
    """

    def ask_for_project_structure(self):
        heading = Figlet(font="slant")
        self.heading(heading.renderText(
            "SpringLeaf CLI"))

        # print(f"\n{CLI.WARNING} Version: {self.version()}\n")
        self.console.print(f"\nVersion: {self.version()}", style="magenta")
        print("")

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

    def heading(self, text):
        self.console.print(text, style="green bold")

    def version(self):
        from version import __version__
        return __version__

    def get_dependencies(self, spring_intializr_file):
        dependencies = []
        for i in spring_intializr_file["dependencies"]["groups"]:
            dependencies.append(Separator(f"▪︎ {i['name']}"))
            for j in i["values"]:
                dependencies.append(j["name"])

        return dependencies

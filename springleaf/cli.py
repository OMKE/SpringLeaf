
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

import springleaf
from pyfiglet import Figlet
from questionary import Separator
from rich.console import Console
from springleaf.generator import Generator
from springleaf.utils.exceptions import InvalidConfigFileException
from springleaf.utils.file_handler import FileHandler
# Handlers
from springleaf.utils.handlers.init_handler import InitHandler
from springleaf.utils.handlers.model_handler import ModelHandler
from springleaf.utils.handlers.spring_initializr_handler import \
    SpringInitializrHandler

from .utils.java_parser import JavaParser
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

    def setup(self):
        if self.args["init"]:
            if(FileHandler.is_spring_dir()):
                if(FileHandler.has_config_file()):
                    if FileHandler.validate_config_file():
                        self.console.print(
                            "Project is already initialized with SpringLeaf", style="green bold")
                    else:
                        self.console.print(
                            "Invalid config file", style="red bold")
                else:
                    self.init_config()
            else:
                self.console.print(
                    "Not a Spring Boot project", style="red bold")
                self.console.print(
                    "Create new project with \n$ springleaf new <name>", style="yellow bold")
        elif self.args["new"]:
            self.spring_intializr(self.args["<name>"])
        elif self.args["generate"]:
            if FileHandler.has_config_file():
                if FileHandler.validate_config_file():
                    self.ask_for_model()
                else:
                    self.console.print("Invalid config file", style="red bold")
            else:
                self.console.print(
                    "Config file is not present. Initialize SpringLeaf with: springleaf init", style="red bold")

    # Spring Intializr

    def spring_intializr(self, project_name):
        if " " in project_name:
            self.console.print(
                "Project name contains spaces", style="red bold")
            return

        # Display heading
        heading = Figlet(font="slant")
        self.heading(heading.renderText(
            "Spring Initializr"))

        # Init new project
        new_project = {
            'name': project_name
        }
        # Read spring_initializr.json and get values
        spring_intializr_file = FileHandler.get_src_file(
            "spring_initializr.json")

        # New line
        print("")
        # Init prompt
        prompt = PromptBuilder().create_question().set_type("select").set_message(
            "Project").set_name("project").set_choices(spring_intializr_file["project"]).create_question().set_type("select").set_message(
            "Spring Boot").set_name("version").set_choices(spring_intializr_file["spring-boot-versions"]).create_question().set_type(
                "text").set_name("description").set_message("Project metadata - Description: ").create_question().set_type(
                    "select").set_message("Packaging").set_name("packaging").set_choices(spring_intializr_file["packaging"]).create_question().set_name(
                        "java_version").set_type(
                    "select").set_message("Java").set_choices(spring_intializr_file["java-version"]).create_question().set_type("checkbox").set_name(
            "dependencies").set_message("Select dependencies").set_choices(self.get_dependencies(spring_intializr_file))

        prompt.set_handler(SpringInitializrHandler, options=new_project)
        # Ask and handle
        prompt.prompt(handle_all=True)

    """
    ask_for_project_structure
    @desc:
        Asks user to select project structure only if config file is not present in cwd
    @return: void - 
    """

    def init_config(self):
        heading = Figlet(font="slant")
        self.heading(heading.renderText(
            "SpringLeaf CLI"))

        # print(f"\n{CLI.WARNING} Version: {self.version()}\n")
        self.console.print(f"\nVersion: {self.version()}", style="magenta")
        print("")
        if self.args["new"]:
            self.console.print(
                "Spring Boot project found, ignoring new command", style="yellow")

        # Reading root package name so user doesn't have to write full package name
        package_name = FileHandler.read_pom_file()["groupId"]

        prompt = PromptBuilder().create_question().set_type("select").set_message("Which project structure to use?").set_name("structure").set_choices(
            self.get_project_structure_names() + [Separator(), {"name": "Don't know which to use?", "disabled": "Check documentation for examples"}]) \
            .create_question().set_type("select").set_message("Constructor, getters and setters").set_name("methods").set_choices(["Standard", "Lombok"]) \
            .create_question().set_type("text").set_message(f"Package name of entity models: {package_name}.").set_name("entities").set_validator("NameValidatorEmpty")

        prompt.set_handler(InitHandler)

        prompt.prompt(handle_all=True)

    def ask_for_model(self):
        try:
            models = FileHandler.get_model_names()
            prompt = PromptBuilder().create_question().set_type("select") \
                .set_message("Select entity model from which you want to generate files").set_name("model").set_choices(models) \
                .set_handler(ModelHandler)
            selected_file = prompt.prompt(handle=True).answers['model']
            # Parse selected file and show model attributes
            # Instantiate JavaParser
            java_parser = JavaParser()
            parsed_attrs = java_parser.parse(selected_file + ".java")
            # Ask for entity attributes which user wants to generate from
            prompt = PromptBuilder().create_question().set_type("checkbox").set_message("Select entity attributes which you want to generate from").set_name("attributes") \
                .set_choices([attr['type'] + ' ' + attr['name'] for attr in parsed_attrs]).set_handler(ModelHandler)
            attributes_answer = prompt.prompt(
                handle=True).answers['attributes']

            if FileHandler.get_from_config_file('structure') == "Standard":
                print("generating for standard")
            elif FileHandler.get_from_config_file('structure') == "Basic":
                print("generating for basic")
            elif FileHandler.get_from_config_file('structure') == "Custom":
                print("generating for custom")

        except InvalidConfigFileException:
            self.console.print(
                "Entity model folder was set but it doesn't exist in path", style="red bold")

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

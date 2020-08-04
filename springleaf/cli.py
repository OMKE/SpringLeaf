
from __future__ import print_function, unicode_literals

import os
from pprint import pprint

import springleaf
from pyfiglet import Figlet
from questionary import Separator
from rich.console import Console
from springleaf.utils.exceptions import InvalidConfigFileException
from springleaf.utils.file_handler import FileHandler
# Handlers
from springleaf.utils.handlers.init_handler import InitHandler
from springleaf.utils.handlers.model_handler import ModelHandler
from springleaf.utils.handlers.spring_initializr_handler import \
    SpringInitializrHandler

from .generator import Generator
from .utils.exceptions import (GeneratorFileExistsException,
                               ModelWithoutAttributesException)
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
                    self.ask_for_model_and_files()
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
            .create_question().set_type("select").set_message("Which controller type are you using?").set_name("controller-type").set_choices(["@Controller", "@RestController"]) \
            .create_question().set_type("select").set_message("Constructor, getters and setters").set_name("methods").set_choices(["Standard", "Lombok"]) \
            .create_question().set_type("text").set_message(f"Package name of entity models: {package_name}.").set_name("entities").set_validator("NameValidatorEmpty") \
            .create_question().set_type("text").set_message("Return type, if you want to use custom generic response class, type full path, if you want to use RespnseEntity leave blank: ").set_name("response")

        prompt.set_handler(InitHandler)

        prompt.prompt(handle_all=True)

    def ask_for_model_and_files(self):
        try:
            models = FileHandler.get_model_names()
            prompt = PromptBuilder().create_question().set_type("select") \
                .set_message("Select entity model from which you want to generate files").set_name("model").set_choices(models) \
                .set_handler(ModelHandler)

            selected_file = None
            # We are catching KeyError Exception because if users cancel the CLI with CTRL + C, at that time we don't have 'model' key in the dict
            try:
                selected_file = prompt.prompt(handle=True).answers['model']
            except KeyError:
                # Disable every action below
                return
            # Parse selected file and show model attributes
            # Instantiate JavaParser
            java_parser = JavaParser()
            attr_choices = []
            # Wrapping in try catch for KeyboardInterrupt Exception
            try:
                try:
                    parsed_attrs = java_parser.parse(selected_file + ".java")
                    attr_choices = [attr['type'] + ' ' +
                                    attr['name'] for attr in parsed_attrs]
                except ModelWithoutAttributesException:
                    self.console.print(
                        "Exception happened during parsing entity model source code. Aborting", style="red bold")
                    return
                # Ask for entity attributes which user wants to generate from
                prompt = PromptBuilder().create_question().set_type("checkbox").set_message("Select entity attributes which you want to generate from").set_name("attributes") \
                    .set_choices(attr_choices).set_handler(ModelHandler)
                attributes_answer = prompt.prompt(
                    handle=True).answers['attributes']

                # We check if user selected any of the choices
                if len(attributes_answer) == 0:
                    self.console.print(
                        "No attributes selected. Aborting!", style="red bold")
                else:
                    if FileHandler.get_from_config_file('structure') == "Standard":
                        # Ask user which file he wants to create, All or selected
                        files_answers = self.ask_for_files("Standard")
                        # We check if user selected any choice
                        if len(files_answers) == 0:
                            self.console.print(
                                "No files selected. Aborting!", style="red bold")
                        else:
                            # Instantiate a generator
                            generator = Generator(selected_file, files_answers, self.get_selected_attrs(
                                parsed_attrs, attributes_answer), "Standard")
                            # List of TemplateUtil, with everything preapred
                            template_utils = generator.prepare_templates_data()

                            for i in template_utils:
                                try:
                                    generator.set_template(
                                        i.template_name + ".java.j2").set_data(i).set_path(i.path).set_name(i.name + ".java").render().generate()

                                    self.console.print(
                                        f"{i.name}.java generated successfully.", style="green bold")

                                except GeneratorFileExistsException:
                                    self.console.print(
                                        f"Error: {i.name}.java already exists", style="red bold")

                    elif FileHandler.get_from_config_file('structure') == "Basic":

                        files_answers = self.ask_for_files("Basic")
                        # We are generating only that user selected
                        # We check if user selected any choice
                        if len(files_answers) == 0:
                            self.console.print(
                                "No files selected. Aborting!", style="red bold")
                        else:
                            # If user selected choices, proceed to generate
                            Generator(selected_file, files_answers, self.get_selected_attrs(
                                parsed_attrs, attributes_answer), "Basic")
                    elif FileHandler.get_from_config_file('structure') == "Custom":
                        print("generating for custom")
                    else:
                        self.console.print(
                            "Invalid project structure, it has to be either Standard, Basic or Custom", style="red bold")
            # We are catching if user press Ctrl+C, exception occurs because we want key from argument dict and it doesn't exist if we cancel the CLI
            except KeyError:
                pass
        except InvalidConfigFileException:
            self.console.print(
                "Entity model folder was set but it doesn't exist in path", style="red bold")

    """
    get_selected_attrs
    @desc:
        Filters out attributes that user selected and returns parsed attrs dict
    @params:
        parsed_attrs - Parsed attributes from JavaParser, 
        selected_attrs - Selected attributes from prompt
    @return: list - list of parsed attributes that user selected
    """

    def get_selected_attrs(self, parsed_attrs, selected_attrs):
        filtered = []
        for i in parsed_attrs:
            for j in selected_attrs:
                if i["name"] == j.split(" ")[1]:
                    filtered.append(i)
                    break
        return filtered

    """
    ask_for_files
    @desc:
        Prompts to user which files he wants to generate
    @return: list - answers that user selected
    """

    def ask_for_files(self, name):

        choices = []

        for key in FileHandler.get_project_structure_content(name).keys():
            if key != "entity" and key != "response":
                if key == "dto":
                    key = key.upper()
                else:
                    key = key.capitalize()
                choices.append(key)

        prompt = PromptBuilder().create_question().set_type("checkbox").set_name("files").set_message("Select which files you want to generate") \
            .set_choices(choices).set_handler(ModelHandler)
        answers = prompt.prompt(handle=True).answers["files"]

        return answers

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

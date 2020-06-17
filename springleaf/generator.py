
import jinja2

from springleaf.utils.exceptions import (GeneratorFileExistsException,
                                         GeneratorFileNameNotFoundException,
                                         GeneratorPathNotFoundException,
                                         TemplateDataNotFoundException,
                                         TemplateNotFoundException)
from springleaf.utils.file_handler import FileHandler
from springleaf.utils.java_parser import JavaParser


class Generator:
    def __init__(self):
        self.java_parser = JavaParser()
        self.output = None

    def generate(self):
        if FileHandler.exists(self.path + "/" + self.name):
            raise GeneratorFileExistsException
        if self.path is None:
            raise GeneratorPathNotFoundException
        if self.name is None:
            raise GeneratorFileNameNotFoundException

        with open(self.path + self.name, "w") as file:
            file.write(self.output)
    """
    #TODO
    @desc:
        Selects a directory structure
    """

    def select_directory_structure(self):
        pass

    def set_template(self, name):
        self.template = jinja2.Template(
            FileHandler.get_template_file(name))
        return self

    def set_data(self, data):
        self.data = data
        return self

    def render(self):
        if self.data is None:
            raise TemplateDataNotFoundException
        if self.template is None:
            raise TemplateNotFoundException

        self.output = self.template.render(data=self.data)

        return self

    def set_path(self, path):
        self.path = path
        return self

    def set_name(self, name):
        self.name = name
        return self

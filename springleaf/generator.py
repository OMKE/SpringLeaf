from springleaf.utils.file_handler import FileHandler
from springleaf.utils.template_util import TemplateUtil

from .base_generator import BaseGenerator


class Generator(BaseGenerator):

    def __init__(self, selected_file, files_to_create, attributes, structure):
        super().__init__()
        self.file = selected_file
        self.files = files_to_create
        self.attributes = attributes
        self.structure = structure

    """
    prepare_templates_data
    @desc:
        Instantiates TemplateUtils with corresponding data
    @return: list - List of TemplateUtil objects
    """

    def prepare_templates_data(self):
        # getting root_package so we can append corespondig sub-package of the file which we have in project_structures.json
        root_package = FileHandler.get_from_config_file('package')
        # Getting type of methods so we can easiy check in the template if it's Standard getters and setters or Lombok
        methods = FileHandler.get_from_config_file('methods')
        # Getting structure content
        structure_content = FileHandler.get_project_structure_content(
            self.structure)
        controller_type = FileHandler.get_from_config_file('controller-type')
        response = FileHandler.get_from_config_file('response')
        template_utils = []

        for i in range(len(self.files)):
            if self.autowire():
                if "Controller" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["service"].replace("&", self.file.lower())))
                elif "Repository" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["entity"]))
                elif "DTO" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["entity"]))
                elif "Mapper" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["entity"] + ":" + root_package + "." + structure_content["dto"]))
                elif "Service" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i] + "Impl", self.files[i] + "Impl",
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["repository"]))
                else:

                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, None))
            else:
                if "Service" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i] + "Impl", self.files[i] + "Impl",
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, self.file + "Repository"))
                elif "Mapper" == self.files[i]:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, root_package + "." + structure_content["entity"] + ":" + root_package + "." + structure_content["dto"]))
                else:
                    template_utils.append(TemplateUtil(self.file + self.files[i], self.files[i],
                                                       self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()], controller_type, response, self.file, None))
        return template_utils

    """
    autowire
    @desc:
        If all files are selected, we can do autowiring automatically
    @return: boolean - True if all are selected, else False
    """

    def autowire(self):
        if len(self.files) == 7:
            return True
        else:
            return False

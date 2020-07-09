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
        self.prepare_templates_data()

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

        template_utils = []
        for i in range(len(self.files)):
            template_utils.append(TemplateUtil(self.file + self.files[i],
                                               self.attributes, methods, root_package + "." + structure_content[self.files[i].lower()]))
        for i in template_utils:
            print(i.name + " " + i.package)
        return template_utils

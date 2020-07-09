

"""
TemplateUtil
@desc:
    Helper class for oop easy accessing data in the template
"""


class TemplateUtil:

    """
    @attributes:
        name - name of the file that should be created and class name
        data - data that template needs
        methods - type of methods we are generating, standard getters and setters or Lombok
        package - package name
    """

    def __init__(self, name: str, data: object, methods: str, package: str):
        self.name = name
        self.data = data
        self.methods = methods
        self.package = package

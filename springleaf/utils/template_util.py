
from .file_handler import FileHandler


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
        controller - controller type, RestController or Controller
        response - return type of controller methods, if user wants to use custom generic class or ResponseEntity
        entity_name - name of the entity class
    """

    def __init__(self, name: str, template_name: str, data: object, methods: str, package: str, controller: str, response: str, entity_name: str, autowire: str):
        self.name = name
        self.template_name = template_name
        self.data = data
        self.methods = methods
        self.package = package
        self.controller = controller
        self.response = response
        self.response_clazz = response.split(
            ".")[-1] if "." in response else "ResponseEntity"
        self.path = "./src/main/java/" + self.package.replace(".", "/") + "/"
        self.entity_name = entity_name
        self.autowire = autowire
        self.service_check()

    """
    service_check
    @desc:
        If file is Service type, we want to create folder in which it will hold two files, interface and implementation
    @return: void - 
    """

    def service_check(self):
        if "&" in self.path and "Service" == self.template_name or "ServiceImpl" == self.template_name:
            self.path = self.path.replace(
                "&", (self.name.replace("Service", "")).replace("Impl", "").lower())
            self.package = self.package.replace(
                "&", (self.name.replace("Service", "")).replace("Impl", "").lower())

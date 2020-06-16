
from ..file_handler import FileHandler
from .handler import Handler


class ProjectStructureHandler(Handler):

    def handle(self, *args):
        if args[0] == "Custom":
            self.use_custom_project_structure()
        else:
            structure = FileHandler.get_project_structure(args[0])
            pom_file = FileHandler.read_pom_file()
            FileHandler.create_config_file({
                "springleaf": {
                    "project": {
                        "name": pom_file["name"],
                        "package": pom_file["groupId"],
                        "structure": structure["name"],
                        "build": self.project_type()
                    }
                }
            })

    def name(self):
        return "structure"

    def use_custom_project_structure(self):
        pass

    def project_type(self):
        if FileHandler.is_maven():
            return "maven"
        elif FileHandler.is_gradle():
            return "gradle"
        else:
            return None

from ..file_handler import FileHandler
from .handler import Handler


class InitHandler(Handler):

    def handle(self, *args):

        if args[0]["structure"] == "Custom":
            self.use_custom_project_structure()
        else:
            structure = FileHandler.get_project_structure(args[0]["structure"])
            pom_file = FileHandler.read_pom_file()

            FileHandler.create_config_file({
                "springleaf": {
                    "project": {
                        "name": pom_file["name"],
                        "package": pom_file["groupId"],
                        "structure": structure["name"],
                        "methods": args[0]["methods"],
                        "entities-folder": args[0]["entities"],
                        "controller-type": args[0]["controller-type"].replace("@", ''),
                        "build": self.project_type(),
                        "response": args[0]['response'] if args[0]['response'] != "" else "ResponseEntity"
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

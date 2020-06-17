
import json
from pprint import pprint

from springleaf.utils.exceptions import GeneratorFileExistsException
from springleaf.utils.file_handler import FileHandler

from .handler import Handler


class SpringInitializrHandler(Handler):

    def __init__(self, options):
        super().__init__(options)

    def name(self):
        return "project"

    def handle(self, *args):
        self.prepare_data(args[0])
        if args[0]["project"] == "Maven Project":
            self.generate_maven_project(args[0])
        else:
            self.generate_gradle_project(args[0])

    def generate_maven_project(self, args):
        self.generate_folder_structure(args)
        self.generate_pom_file(self.prepare_data(args, pom_file=True))
        self.generate_application_file(self.prepare_data(args))
        self.generate_servlet_init_file(self.prepare_data(args))
        self.generate_inital_test_file(self.prepare_data(args))

    def generate_gradle_project(self, args):
        self.exception("Gradle will be supported in future versions")

    """
    generate_folder_structure
    @desc:
        Generates folder structure
    @return: void - 
    """

    def generate_folder_structure(self, args):
        name = self.get_name()
        name_without_dash = self.get_name(strip_dash=True)
        self.unzip_build_tools_for_maven(name + "/")
        FileHandler.create_folder_structure(
            f"{name}/src/main/java/com/{name_without_dash}")
        FileHandler.create_folder_structure(
            f"{name}/src/main/resources/static"
        )
        FileHandler.create_folder_structure(
            f"{name}/src/main/resources/templates"
        )
        FileHandler.create_folder_structure(
            f"{name}/src/test/java/com/{name_without_dash}"
        )

    """
    generate_pom_data
    @desc:
        Generates pom.xml file with given data
    @raises:
        GeneratorFileExistsException - if pom file already exists
    @return: void - 
    """

    def generate_pom_file(self, data):
        try:
            self.generator.set_template("pom.xml.j2").set_data(data).set_path(self.get_name() + "/") \
                .set_name("pom.xml").render().generate()
        except GeneratorFileExistsException:
            self.exception("Pom file exists. Aborting")

    def generate_application_file(self, data):
        data["name"] = self.get_application_name()
        try:
            self.generator.set_template("Application.java.j2").set_data(data) \
                .set_path(self.get_name() + "/src/main/java/com/" + self.get_name(strip_dash=True) + "/") \
                .set_name(self.get_application_name() + "Application.java").render().generate()
        except GeneratorFileExistsException:
            self.exception("Application file exists. Aborting")

    def generate_servlet_init_file(self, data):
        data["name"] = self.get_application_name() + "Application"
        try:
            self.generator.set_template("ServletInitializer.java.j2").set_data(data) \
                .set_path(self.get_name() + "/src/main/java/com/" + self.get_name(strip_dash=True) + "/") \
                .set_name("ServletInitializer.java").render().generate()
        except GeneratorFileExistsException:
            self.exception("Application file exists. Aborting")

    def generate_inital_test_file(self, data):
        data["name"] = self.get_application_name()
        try:
            self.generator.set_template("ApplicationTests.java.j2").set_data(data) \
                .set_path(self.get_name() + "/src/test/java/com/" + self.get_name(strip_dash=True) + "/") \
                .set_name(self.get_application_name() + "ApplicationTests.java").render().generate()
        except GeneratorFileExistsException:
            self.exception("Application file exists. Aborting")

    """
    prepare_data
    @desc:
        Prepares data as dictionary so we can use it in the template
    @return: dict - 
    """

    def prepare_data(self, args, pom_file=False):

        java_version: str = args["version"]
        spring_boot: str = args["version"]

        description: str = args["description"]
        packaging: str = args["packaging"]
        name: str = self.get_name()
        groupId: str = f"com.{name}".replace(
            "-", "").replace(" ", "").strip('"')
        data = args

        if java_version == "8":
            data["java_version"] = "1.8"

        # Resolve versioning
        if pom_file:
            data["version"] = spring_boot + ".RELEASE"

        if description == "":
            data["description"] = name + " project initialized with SpringLeaf"

        data["groupId"] = groupId
        data["name"] = name
        data["artifact"] = name
        data['packaging'] = packaging.lower()
        if pom_file:
            data['dependencies'] = self.parse_dependencies(
                args['dependencies'])

        return data

    """
    get_name
    @desc:
        returns name from passed options
    @return: str - name
    """

    def get_name(self, strip_dash=False, intial=False):
        if intial:
            return self.options["name"]
        if strip_dash:
            return self.options["name"].replace(" ", "").replace("-", "").strip('"')
        return self.options["name"].replace(" ", "").strip('"')

    def get_application_name(self):
        name: str = self.get_name()
        return name.title().replace("-", "").replace("_", "").strip('"')

    """
    parse_dependencies
    @desc:
        Gets dependencies as a list ["Spring DevTools", "Spring Security", "Spring Web"], reads from spring_initializr.json and returns corresponding values
    @return: list - list of dicts with form 
    {
        "name": "<name>",
        "attributes: [
            "name": "<name>",
            "value": "<value>"
        ]
    }
    """

    def parse_dependencies(self, deps):
        dependencies = []
        groups = FileHandler.get_src_file(
            "spring_initializr.json")["dependencies"]["groups"]

        for dep in deps:
            for j in groups:
                for k in j["values"]:
                    if k["name"] == dep:
                        dependencies.append(k)
        return dependencies

    def unzip_build_tools_for_maven(self, extract_dir):
        FileHandler.unzip_file(extract_dir, "build-maven.zip")

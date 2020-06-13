from json import dumps, loads
from pprint import pprint

from javalang.parse import parse
from springleaf.utils.file_handler import FileHandler


class JavaParser:

    """
    parse
    @desc:
        Parses file with javalang, returns Class attributes
    @params:
        file_name - name of the file
    @return: list - [
        {
            name = <attribute_name>
            type = <type>
            sub_types = [<type>, <type>] - if type is collection
        }
    ]
    """
    """
    
    #FIXME
    #BUG
    @desc:
        If model has an attribute with nested types like HashMap<String, HashMap<String, String>> it doesn't return nested types
        Until it's not fixed, ask user to ignore this attribute
    """

    def parse(self, file_name):
        attributes = []

        json = dumps(self.get_parsed_file(self.file(file_name)),
                     sort_keys=True, default=JavaParser.json_ast_encoder)
        load = loads(json)
        for i in load["types"]:
            for j in i["body"]:
                for k in j["declarators"]:
                    attribute = {}
                    attribute["name"] = k["name"]
                    attribute['sub_types'] = []
                    # Field is None if type is not collection
                    if j["type"]['arguments'] == None:
                        attribute["type"] = j["type"]["name"]
                    else:

                        attribute['type'] = j['type']['name']
                        for l in j['type']['arguments']:
                            attribute['sub_types'].append(l['type']['name'])

                    attributes.append(attribute)
        pprint(attributes)

    @staticmethod
    def json_ast_encoder(o):
        if type(o) is set and len(o) == 0:
            return []
        if hasattr(o, "__dict__"):
            return o.__dict__
        return ""

    """
    get_package
    @desc:
        Gets package name of file
    @params:
        path [FileHandler.current_dir()] - path of file, if nothing passed current working directory will be used
    @return: string - package name
    """

    def get_package(self, path=FileHandler.current_dir()):
        main_class = FileHandler.get_first_file_in_tree(path)
        file_to_parse = FileHandler.read_file(main_class)
        return parse(file_to_parse).package.name

    """
    get_parsed_file
    @desc:
        Finds file with given name and returns CompilationUnit
    @params:
        model_name - Model name, 
    @return: CompilationUnit - parsed file
    """

    def get_parsed_file(self, model_name):
        current_dir = FileHandler.current_dir()
        file_to_parse = FileHandler.read_file(
            FileHandler.search(current_dir, model_name, True))
        return parse(file_to_parse)

    """
    file
    @desc:
        Check for passed file name, if passed without .java extension, it will be apended, else will return passed
    @params:
        file_name -  name of the file, 
    @return:  string - file_name formated if needed
    """

    def file(self, file_name: str):
        if ".java" in file_name:
            return file_name
        else:
            return "{name}.java".format(name=file_name)

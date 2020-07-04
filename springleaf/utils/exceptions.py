

class QuestionNotCreatedException(Exception):
    pass


class TemplateNotFoundException(Exception):
    pass


class TemplateDataNotFoundException(Exception):
    pass


class GeneratorPathNotFoundException(Exception):
    pass


class GeneratorFileNameNotFoundException(Exception):
    pass


class GeneratorFileExistsException(Exception):
    pass


class InvalidConfigFileException(Exception):
    pass


class ModelWithoutAttributesException(Exception):
    pass

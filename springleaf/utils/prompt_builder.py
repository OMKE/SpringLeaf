
from __future__ import print_function, unicode_literals

from prompt_toolkit.styles import Style
from questionary import Choice, Separator, ValidationError, Validator, prompt

from springleaf.utils.exceptions import QuestionNotCreatedException

# from prompt_toolkit.styles import Style


class NameValidatorLessThan3(Validator):
    def validate(self, document):
        if len(document.text) < 3:
            raise ValidationError(
                message="Name can not be shorter than 3 chars",
                cursor_position=len(document.text)
            )


class NameValidatorEmpty(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message="Field cannot be empty",
                cursor_position=len(document.text)
            )


class GroupNameValidator(Validator):
    def validate(self, document):
        if " " in document.text:
            raise ValidationError(
                message="Group name cannot contain spaces", cursor_position=len(document.text))


style = Style([
    ('separator', 'fg:#fcba03')
])


class PromptBuilder:

    def __init__(self):
        self.questions = []
        self.handlers = []

    def create_question(self):
        self.questions.append({})
        return self

    def get_question(self):
        try:
            return self.questions[-1]
        except IndexError:
            raise QuestionNotCreatedException

    def set_heading(self, message):
        print(message)
        return self

    def set_type(self, type):
        self.get_question()["type"] = type

        return self

    def set_message(self, message):

        self.get_question()["message"] = message

        return self

    def set_name(self, name):

        self.get_question()["name"] = name

        return self

    def set_choices(self, choices):

        self.get_question()["choices"] = [choice for choice in choices]

        return self

    def validator(self, name):
        validators = {
            "NameValidatorLessThan3": NameValidatorLessThan3,
            "NameValidatorEmpty": NameValidatorEmpty,
            "GroupNameValidator": GroupNameValidator
        }
        return validators[name]

    def set_validator(self, name):

        self.get_question()["validate"] = self.validator(name)

        return self

    def set_default(self, index):

        self.get_question()["default"] = index

        return self

    def set_handler(self, handler, options=None):
        self.handlers.append(handler(options))
        return self

    """
    prompt
    @desc:
        Initializes prompt
    @return: PromptBuilder - self
    """

    def prompt(self, handle=False, handle_all=False):
        self.answers = prompt(self.questions, style=style)
        if handle:
            self.handle()
        elif handle_all:
            self.handle_many()
        return self

    """
    handle
    @desc:
        Maps handlers to questions
    @return: void - 
    """

    def handle(self):
        for handler in self.handlers:
            for _ in self.answers:
                handler.handle(dict(self.answers).get(handler.name()))
                break

    def handle_many(self):
        for handler in self.handlers:
            for _ in self.answers:
                handler.handle(self.answers)
                break

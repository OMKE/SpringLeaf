
from __future__ import print_function, unicode_literals

from questionary import Choice, Separator, prompt

from springleaf.utils.exceptions import QuestionNotCreatedException

# from prompt_toolkit.styles import Style



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
            "NameValidator": NameValidator
        }
        return validators[name]

    def set_validator(self, name):

        self.get_question()["validate"] = self.validator(name)

        return self

    def set_default(self, bool=False):

        self.get_question()["default"] = bool

        return self

    def set_handler(self, handler):
        self.handlers.append(handler())
        return self

    """
    prompt
    @desc:
        Initializes prompt
    @return: PromptBuilder - self
    """

    def prompt(self, handle=False):
        self.answers = prompt(self.questions)
        if handle:
            self.handle()
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

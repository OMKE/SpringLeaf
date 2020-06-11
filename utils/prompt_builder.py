
from __future__ import print_function, unicode_literals

from PyInquirer import (Separator, Token, ValidationError, Validator, prompt,
                        style_from_dict)


class PromptBuilder:

    FAIL = '\033[91m'

    def __init__(self):
        self.question = {}
        self.handler = None
        self.style = style_from_dict({
            Token.Pointer: "#83E774",
            Token.QuestionMark: "#ffd738"
        })

    def add_type(self, type):
        self.question["type"] = type
        return self

    def add_message(self, message):
        self.question["message"] = message
        return self

    def add_name(self, name):
        self.question["name"] = name
        return self

    def add_choices(self, choices):
        self.question["choices"] = [choice for choice in choices]
        return self

    def add_validator(self, validator):
        self.question["validate"] = validator
        return self

    def add_default(self, bool=False):
        self.question["default"] = bool

    def add_handler(self, handler):
        self.handler = handler()
        return self

    def ask(self):
        self.answers = prompt([self.question], style=self.style)
        return self

    def handle(self):
        try:
            try:
                self.handler.handle(self.answers)
            except AttributeError:
                print(
                    f"{PromptBuilder.FAIL} Handlers were called but prompt wasn't initialized")
        except KeyError:
            self.handler.handle(self.answers)

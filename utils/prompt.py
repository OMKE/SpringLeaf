
from __future__ import print_function, unicode_literals

from PyInquirer import Separator, Token, prompt, style_from_dict


class Prompt:

    def __init__(self):
        self.questions = []

    def style(self):
        return style_from_dict({
            Token.Pointer: "#83E774"
        })

    def add_question(self, type, message, name, choices, validate=None):

        return self.questions.append({
            'type': type,
            'name': name,
            'message': message,
            'choices': [choice for choice in choices],
            'validate': validate
        })

    def get_questions(self):
        return self.questions

    def ask(self):
        return prompt(self.get_questions(), style=self.style())

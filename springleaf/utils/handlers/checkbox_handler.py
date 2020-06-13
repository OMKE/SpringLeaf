
from .handler import Handler


class CheckBoxHandler(Handler):

    def handle(self, *args):
        print("CheckboxHandler" + str(args))

    def name(self):
        return "options"

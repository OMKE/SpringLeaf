
from .handler import Handler


class NameHandler(Handler):

    def handle(self, *args):
        print("NH" + str(args))

    def name(self):
        return "name"

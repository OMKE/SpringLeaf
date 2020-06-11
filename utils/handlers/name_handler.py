
from .handler import Handler


class NameHandler(Handler):

    def handle(self, *args):
        print(args)

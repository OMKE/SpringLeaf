
from rich.console import Console

from springleaf.generator import Generator


class Handler:

    def __init__(self, options):
        self.generator = Generator()
        self.options = options

    """
    name
    @desc:
        Should return a question name on which this handler will get data from 
    @return: string - name
    """

    def name(self):
        raise NotImplementedError(
            "Every handler should return name of question to handle")

    def handle(self, *args):
        raise NotImplementedError("Hanlder is set but it's not implemented")

    def exception(self, message):
        Console().print(message, style="red bold")

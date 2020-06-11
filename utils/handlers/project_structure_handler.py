
from .handler import Handler


class ProjectStructureHandler(Handler):
    def __init__(self):
        super().__init__()

    def handle(self, *args):
        print(args)

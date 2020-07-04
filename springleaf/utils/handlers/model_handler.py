from .handler import Handler


class ModelHandler(Handler):

    def name(self):
        return "model"

    def handle(self, *args):
        return args[0]

from PyInquirer import ValidationError


class Handler:

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

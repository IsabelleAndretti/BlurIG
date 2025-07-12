
class Error_model:
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def show(self):
        return {self.message}, self.code
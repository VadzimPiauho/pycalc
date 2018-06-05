class MyException(Exception):
    """Exception """
    message = "Error: {}"

    def __init__(self, name):
        self.name = name
        self.message = self.message.format(name)

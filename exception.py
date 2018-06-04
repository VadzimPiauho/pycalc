class MyException(Exception):
    """Exception """
    message = "Error: {}"

    def __init__(self, name):
        self.name = name
        self.message = self.message.format(name)

    # def __str__(self):
    #     print(self.message)

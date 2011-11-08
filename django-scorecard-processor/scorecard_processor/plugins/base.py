from register import register
class Plugin:
    name = "Dummy plugin"
    def __init__(self, operation):
        self.operation = operation

    def process(self):
        raise NotImplementedError 

    def num_arguments():
        return 2

register('dummy','dummy',Plugin)

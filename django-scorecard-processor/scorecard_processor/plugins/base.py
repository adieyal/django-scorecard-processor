from register import register
class Plugin:
    def __init__(self, operation):
        self.operation = operation

    def process(self):
        raise NotImplementedError 

register('dummy','dummy',Plugin)

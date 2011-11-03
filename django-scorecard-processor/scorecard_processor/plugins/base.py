class Plugin:
    def __init__(self, operation):
        self.operation = operation

    def process(self):
        raise NotImplementedError 

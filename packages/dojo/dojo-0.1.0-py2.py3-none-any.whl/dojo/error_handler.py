
class MockErrorHandler(object):

    def __init__(self):
        self.errors = []

    def capture(self, error):
        self.errors.append(error)

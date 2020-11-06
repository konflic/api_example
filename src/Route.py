from src.settings import HTTP_METHODS

class Route:

    def __init__(self, path, methods=HTTP_METHODS, params=None, description=None):
        self.path = path
        self.methods = methods
        self.params = params
        self.description = description

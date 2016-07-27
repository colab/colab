class PluginDoesNotExistError(KeyError):
    def __init__(self, message):
        super(KeyError, self).__init__(message)

class ApilibException(Exception):
    pass


class UnknownFieldException(ApilibException):
    pass

class ModuleRequired(ApilibException):
    pass

class ConfigurationRequired(ApilibException):
    pass

class NotInitialized(ApilibException):
    pass

class ModelLoadingError(ApilibException):
    # Needs to be overridden
    ERROR_NAME = None

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return '%s:\n  %s' % (
            self.ERROR_NAME,
            '\n  '.join(str(e) for e in self.errors),
        )

class DeserializationError(ModelLoadingError):
    ERROR_NAME = 'DeserializationError'

class ValidationError(ModelLoadingError):
    ERROR_NAME = 'ValidationError'


class MethodNotFoundException(ApilibException):
    pass

class MethodNotImplementedException(ApilibException):
    pass

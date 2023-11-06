class ResourceNotFound(Exception):
    pass


class ResourceAlreadyExists(Exception):
    pass


class ApplicationValidationError(Exception):
    pass


class UncaughtApplicationError(Exception):
    pass

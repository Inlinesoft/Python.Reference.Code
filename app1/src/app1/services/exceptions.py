class BaseServiceException(Exception):
    def __str__(self):
        message = " ".join(self.args)
        return f"{self.__class__.__name__} - {message}"


class ProductNotConfigured(BaseServiceException):
    pass


class MissingDataError(BaseServiceException):
    pass


class MissingRunError(BaseServiceException):
    pass


class RunEarlierThanInitialDate(BaseServiceException):
    pass


class RunDateIsHoliday(BaseServiceException):
    pass


class RunAlreadyPerformed(BaseServiceException):
    pass

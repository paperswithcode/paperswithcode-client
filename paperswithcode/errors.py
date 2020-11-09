__all__ = ["PapersWithCodeError", "ReadOnlyPropertyError", "ValidationError"]

from tea_client.errors import TeaClientError


PapersWithCodeError = TeaClientError


class ReadOnlyPropertyError(PapersWithCodeError):
    def __init__(self, message):
        super(ReadOnlyPropertyError, self).__init__(message=message)


class ValidationError(PapersWithCodeError):
    def __init__(self, message):
        super(ValidationError, self).__init__(message=message)

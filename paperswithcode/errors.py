from requests import Response


class PapersWithCodeError(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.name}(message={self.message})"

    __repr__ = __str__


class HttpClientError(PapersWithCodeError):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response: Response = response
        self.status_code = (
            response.status_code if response is not None else 500
        )

    @property
    def data(self):
        return self.response.json()

    def __str__(self):
        return (
            f"{self.name}(message={self.message}, "
            f"status_code={self.status_code})"
        )

    __repr__ = __str__


class HttpClientTimeout(HttpClientError):
    """Http timeout error.

    From http://docs.python-requests.org/en/master/user/quickstart/#timeouts:

        timeout is not a time limit on the entire response download; rather, an
        exception is raised if the server has not issued a response for timeout
        seconds (more precisely, if no bytes have been received on the
        underlying socket for timeout seconds). If no timeout is specified
        explicitly, requests do not time out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.

    ConnectTimeout:
        The request timed out while trying to connect to the remote server.
        Requests that produced this error are safe to retry.

    ReadTimeout:
        The server did not send any data in the allotted amount of time.
    """

    def __init__(self):
        super().__init__("Timeout exceeded")


class HttpRateLimitExceeded(HttpClientError):
    def __init__(self, response, limit, remaining, reset, retry):
        super().__init__("Rate limit exceeded.", response=response)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.retry = retry

    def __str__(self):
        return (
            f"{self.name}(limit={self.limit}, remaining={self.remaining}, "
            f"reset={self.reset}s, retry={self.retry}s)"
        )

    __repr__ = __str__


class SerializationError(PapersWithCodeError):
    def __init__(self, errors):
        """Thrown when the client cannot serialize or deserialize an object.

        Args:
            errors (dict): Dictionary of found errors
        """
        super().__init__("Serialization error.")
        self.errors = errors

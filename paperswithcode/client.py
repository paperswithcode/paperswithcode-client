from paperswithcode.config import Config


class Client(object):
    """PapersWithCode client.

    Args:
        config (paperswithcode.config.Config): Instance of the paperswithcode
            configuration.
    """

    def __init__(self, config: Config):
        self.config = config

        from paperswithcode.http import HttpClient

        self.http = HttpClient(url=config.url, token=config.token)

    @classmethod
    def public(cls) -> "Client":
        """Get the public access paperswithcode client.

        Returns:
            Client: A client instance that can be used to make public API
                requests to paperswithcode.com.
        """
        config = Config(None)
        return Client(config)

    def login(self, username: str, password: str) -> str:
        """Obtain authentication token.

        Args:
            username (str): PapersWithCode username.
            password (str): PapersWithCode password.

        Returns:
            str: Authentication token.
        """
        response = self.http.post(
            "auth/token/", data={"username": username, "password": password}
        )
        return response["token"]

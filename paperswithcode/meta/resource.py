import logging


logger = logging.getLogger(__name__)


class Resource(object):
    """Resource is a utility class for fetching data using the API server."""

    def __init__(self, urls, api):
        self.data = {}
        self.urls = urls
        self.api = api
        self.fetched = False

    def fetch(self, item=None):

        logger.debug(
            f"Property '{item}' is not set, fetching resource from server"
            if item
            else "Requested property is not set, fetching resource from server"
        )

        uri = self.data.get("uri", None)

        if uri is not None:
            self.data = self.api.get(uri)
            logger.debug("Resource fetched using the 'uri' property.")
        elif self.urls is not None and "get" in self.urls:
            resource_id = self.data.get("id", None)
            if resource_id is None:
                logger.debug(
                    "Failed to fetch resource, neither 'id' nor 'uri' property"
                    " is set"
                )
                return
            self.data = self.api.get(self.urls["get"].format(id=resource_id))
            logger.debug("Resource fetched using the id property.")
        else:
            logger.debug(
                "Skipping resource fetch, retrieval for this resource is "
                "not available."
            )
            return
        self.fetched = True

    def __getitem__(self, item):
        if item not in self.data and not self.fetched:
            self.fetch(item=item)
        try:
            return self.data[item]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        self.data[key] = value

from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Dataset(TeaClientModel):
    """Dataset object.

    Attributes:
        id (str): Dataset ID.
        name (str): Dataset name.
        url (str, optional): URL for dataset download.
    """

    id: str
    name: str
    url: Optional[str]


class Datasets(Page):
    """Object representing a paginated page of datasets.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Dataset]): List of datasets on this page.
    """

    results: List[Dataset]

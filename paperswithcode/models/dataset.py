from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Dataset(TeaClientModel):
    """Dataset object.

    Attributes:
        id (str): Dataset ID.
        name (str): Dataset name.
        full_name (str, optional): Dataset full name.
        url (str, optional): URL for dataset download.
    """

    id: str
    name: str
    full_name: Optional[str]
    url: Optional[str]


class DatasetCreateRequest(TeaClientModel):
    """Task object.

    Attributes:
        name (str): Dataset name.
        full_name (str, optional): Dataset full name.
        url (str, optional): Dataset url.
    """

    name: str
    full_name: Optional[str] = None
    url: Optional[str] = None


class DatasetUpdateRequest(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        name (str, optional): Dataset name.
        url (str, optional): Dataset url.
    """

    name: Optional[str] = None
    url: Optional[str] = None


class Datasets(Page):
    """Object representing a paginated page of datasets.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Dataset]): List of datasets on this page.
    """

    results: List[Dataset]

from typing import List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Author(TeaClientModel):
    """Author object.

    Attributes:
        id (str): Author ID.
        full_name (str, optional): Author full name.
    """

    id: str
    full_name: str


class Authors(Page):
    """Object representing a paginated page of authors.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Author]): List of authors on this page.
    """

    results: List[Author]

from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Conference(TeaClientModel):
    """Conference object.

    Attributes:
        id (str): Conference ID.
        name (str): Conerence name.
    """

    id: str
    name: str


class Conferences(Page):
    """Object representing a paginated page of conferences.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Conference]): List of conferences on this page.
    """

    results: List[Conference]


class Proceeding(TeaClientModel):
    """Conference proceeding object.

    Attributes:
        id (str): Proceeding ID.
        year (int, optinoal): Year in which the proceeding was held.
        month (int, optional): Month in which the proceedingt was held.
    """

    id: str
    year: Optional[int]
    month: Optional[int]


class Proceedings(Page):
    """Object representing a paginated page of proceedings.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Proceeding]): List of proceedings on this page.
    """

    results: List[Proceeding]

from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page
from paperswithcode.models.paper import Paper
from paperswithcode.models.repository import Repository


class PaperRepo(TeaClientModel):
    """Paper <-> Repository object.

    Attributes:
        paper (Paper): Paper objects.
        repository (Repository, optional): Repository object.
        is_official (bool): Is this the official implementation.
    """

    paper: Paper
    repository: Optional[Repository]
    is_official: bool


class PaperRepos(Page):
    """Object representing a paginated page of paper<->repos.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[PaperRepo]): List of paper<->repos on this page.
    """

    results: List[PaperRepo]

from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Repository(TeaClientModel):
    """Repository object.

    Attributes:
        url (str): URL of the repository.
        owner (str): Repository owner.
        name (str): Repository name.
        description (str): Repository description.
        stars (int): Number of repository stars.
        framework (str): Implementation framework (TensorFlow, PyTorch, MXNet,
            Torch, Jax, Caffee2...).
        is_official (bool): Is this an official implementation of the paper.
            Available only when listing repositories for a specific paper.
    """

    url: str
    owner: str
    name: str
    description: str
    stars: int
    framework: str
    is_official: Optional[bool]


class Repositories(Page):
    """Object representing a paginated page of repositories.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Repository]): List of repositories on this page.
    """

    results: List[Repository]

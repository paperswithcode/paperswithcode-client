from typing import List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Repository(TeaClientModel):
    """Repository object.

    Attributes:
        url (str): URL of the repository.
        is_official (bool): Is this an official implementation of the paper.
        description (str): Repository description.
        stars (int): Number of repository stars.
        framework (str): Implementation framework (TensorFlow, PyTorch, MXNet,
            Torch, Jax, Caffee2...)
    """

    url: str
    is_official: bool
    description: str
    stars: int
    framework: str


class Repositories(Page):
    """Object representing a paginated page of repositories.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Repository]): List of repositories on this page.
    """

    results: List[Repository]

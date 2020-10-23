from datetime import date
from typing import Optional, List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Paper(TeaClientModel):
    """Paper object.

    Attributes:
        id (str): Paper ID.
        arxiv_id (str, optional): ArXiv ID.
        nips_id (str, optional): NIPS Conference ID.
        url_abs (str): URL to the paper abstract.
        url_pdf (str): URL to the paper PDF.
        title (str): Paper title.
        abstract (str): Paper abstract.
        authors (List[str]): List of paper authors.
        published (date): Paper publication date.
        conference (str, optional): ID of the conference in which the paper was
            published.
        conference_url_abs (str, optional): URL to the conference paper page.
        conference_url_pdf (str, optional): URL to the conference paper PDF.
        proceeding (str, optional): ID of the conference proceeding in which
            the paper was published.
    """

    id: str
    arxiv_id: Optional[str]
    nips_id: Optional[str]
    url_abs: str
    url_pdf: str
    title: str
    abstract: str
    authors: List[str]
    published: date
    conference: Optional[str]
    conference_url_abs: Optional[str]
    conference_url_pdf: Optional[str]
    proceeding: Optional[str]


class Papers(Page):
    """Object representing a paginated page of papers.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Paper]): List of papers on this page.
    """

    results: List[Paper]

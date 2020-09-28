from datetime import date
from typing import Optional, List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Paper(TeaClientModel):
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
    results: List[Paper]

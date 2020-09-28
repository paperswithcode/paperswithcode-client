from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Conference(TeaClientModel):
    id: str
    name: str


class Conferences(Page):
    results = List[Conference]


class Proceeding(TeaClientModel):
    id: str
    year: Optional[int]
    month: Optional[int]


class Proceedings(Page):
    results = List[Proceeding]

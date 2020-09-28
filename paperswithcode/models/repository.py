from typing import List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Repository(TeaClientModel):
    url: str
    is_official: bool
    description: str
    stars: int
    framework: str


class Repositories(Page):
    results = List[Repository]

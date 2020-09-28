from typing import List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Area(TeaClientModel):
    id: str
    name: str


class Areas(Page):
    results = List[Area]


class Task(TeaClientModel):
    id: str
    name: str
    description: str


class Tasks(Page):
    results = List[Task]

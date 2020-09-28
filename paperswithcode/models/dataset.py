from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Dataset(TeaClientModel):
    id: str
    name: str
    url: Optional[str]


class Datasets(Page):
    results = List[Dataset]

from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Method(TeaClientModel):
    id: str
    name: str
    full_name: str
    description: str
    paper: Optional[str]


class Methods(Page):
    results = List[Method]

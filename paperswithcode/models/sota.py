from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class SotaPartial(TeaClientModel):
    id: str
    task: str
    dataset: str


class SotaPartials(Page):
    results = List[SotaPartial]


class Metric(TeaClientModel):
    name: str
    description: str
    is_loss: bool


class Row(TeaClientModel):
    best_rank: Optional[int]
    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]
    best_metric: Optional[str]


class Sota(TeaClientModel):
    id: str
    task: str
    dataset: str
    metrics: List[Metric]
    rows: List[Row]

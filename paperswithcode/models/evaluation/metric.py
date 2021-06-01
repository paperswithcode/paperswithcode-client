from typing import Optional, List

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class Metric(TeaClientModel):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        id (str): Metric id.
        name (str): Metric name.
        description (str): Metric description.
        is_loss (bool): Is this a loss metric.
    """

    id: str
    name: str
    description: str
    is_loss: bool


class Metrics(Page):
    """Object representing a paginated page of metrics.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[Metric]): List of metrics on this page.
    """

    results: List[Metric]


class MetricCreateRequest(TeaClientModel):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name (str): Metric name.
        description (str): Metric description.
        is_loss (bool): Is this a loss metric.
    """

    name: str
    description: str
    is_loss: bool


class MetricUpdateRequest(TeaClientModel):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name (str, optional): Metric name.
        description (str, optional): Metric description.
        is_loss (bool, optional): Is this a loss metric.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_loss: Optional[bool] = None

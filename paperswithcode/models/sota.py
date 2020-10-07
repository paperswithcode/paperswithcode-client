from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class SotaPartial(TeaClientModel):
    """Evaluation table object.

    Short version used for listing.

    Attributes:
        id (str): Evaluation table ID.
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
    """

    id: str
    task: str
    dataset: str


class SotaPartials(Page):
    """Object representing a paginated page of evaluation tables.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[SotaPartial]): List of evaluation tables on this page.
    """

    results: List[SotaPartial]


class Metric(TeaClientModel):
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


class Result(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        best_rank (int, optional): Best rank of the row.
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        best_metric (str, optional): Name of the best metric.
    """

    best_rank: Optional[int]
    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]
    best_metric: Optional[str]


class Sota(TeaClientModel):
    """Evaluation table object.

    Attributes:
        id (str): ID of the evaluation table.
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
        metrics (List[Metric]): List of metrics used in evaluation.
        rows (List[Row]) List of evaluation rows.
    """

    id: str
    task: str
    dataset: str
    metrics: List[Metric]
    rows: List[Result]

from typing import Optional

from tea_client.models import TeaClientModel


class Result(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        id (str): Result id.
        best_rank (int, optional): Best rank of the row.
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        best_metric (str, optional): Name of the best metric.
    """

    id: str
    best_rank: Optional[int]
    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]
    best_metric: Optional[str]


class ResultCreateRequest(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
    """

    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]


class ResultUpdateRequest(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        metrics (dict, optional): Dictionary of metrics and metric values.
        methodology (str, optional): Methodology used for this implementation.
        uses_additional_data (bool, optional): Does this evaluation uses
            additional data not provided in the dataset used for other
            evaluations.
        paper (str, optional): Paper describing the evaluation.
    """

    metrics: Optional[dict] = None
    methodology: Optional[str] = None
    uses_additional_data: Optional[bool] = None
    paper: Optional[str] = None

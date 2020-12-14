from datetime import datetime
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
        evaluation_date (datetime, optional): Date of the result evaluation.
    """

    id: str
    best_rank: Optional[int]
    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]
    best_metric: Optional[str]
    evaluation_date: Optional[datetime]


class _ResultRequest(TeaClientModel):
    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        d = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        evaluation_date = d.get("evaluation_date")
        if isinstance(evaluation_date, datetime):
            d["evaluation_date"] = evaluation_date.strftime("%Y-%m-%d")
        return d


class ResultCreateRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        evaluation_date (datetime, optional): Date of the result evaluation.
    """

    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str] = None
    evaluation_date: Optional[datetime] = None


class ResultUpdateRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics (dict, optional): Dictionary of metrics and metric values.
        methodology (str, optional): Methodology used for this implementation.
        uses_additional_data (bool, optional): Does this evaluation uses
            additional data not provided in the dataset used for other
            evaluations.
        paper (str, optional): Paper describing the evaluation.
        evaluation_date (datetime, optional): Date of the result evaluation.
    """

    metrics: Optional[dict] = None
    methodology: Optional[str] = None
    uses_additional_data: Optional[bool] = None
    paper: Optional[str] = None
    evaluation_date: Optional[datetime] = None

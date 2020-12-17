from typing import Optional, List

from pydantic import Field

from tea_client.models import TeaClientModel

from paperswithcode.models.evaluation.result import _ResultRequest


class ResultSyncRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
        evaluated_on (str): Evaluation date in YYYY-MM-DD format
        external_source_url (str, option): The URL to the external source (eg competition)
    """

    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""
    evaluated_on: str
    external_source_url: Optional[str] = None


class MetricSyncRequest(TeaClientModel):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name (str): Metric name.
        description (str): Metric description.
        is_loss (bool): Is this a loss metric.
    """

    name: str
    description: str = ""
    is_loss: bool = True


class EvaluationTableSyncRequest(TeaClientModel):
    """Evaluation table object.

    Attributes:
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
        description (str): Evaluation table description.
        mirror_url (str, optional): URL to the evaluation table that this table
            is a mirror of.
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
        metric (list): List of MetricSyncRequest objects used in the evaluation.
        results (list): List of ResultSyncRequest objects - results of the
            evaluation.
    """

    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None
    external_id: Optional[str] = None
    metrics: List[MetricSyncRequest] = Field(default_factory=list)
    results: List[ResultSyncRequest] = Field(default_factory=list)


class ResultSyncResponse(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        id (str): Result id.
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
        evaluated_on (str, optional): Evaluation date in YYYY-MM-DD format
        external_source_url (str, option): The URL to the external source (eg competition)
    """

    id: str
    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""
    evaluated_on: Optional[str] = None
    external_source_url: Optional[str] = None


class MetricSyncResponse(TeaClientModel):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name (str): Metric name.
        description (str): Metric description.
        is_loss (bool): Is this a loss metric.
    """

    name: str
    description: str = ""
    is_loss: bool = True


class EvaluationTableSyncResponse(TeaClientModel):
    """Evaluation table object.

    Attributes:
        id (str): Evaluation table ID.
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
        description (str): Evaluation table description.
        mirror_url (str, optional): URL to the evaluation table that this table
            is a mirror of.
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
        metric (list): List of metrics sync objects used in the evaluation.
        results (list): List of result sync objects - results of the
            evaluation.
    """

    id: str
    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None
    external_id: Optional[str] = ""
    metrics: List[MetricSyncResponse] = Field(default_factory=list)
    results: List[ResultSyncResponse] = Field(default_factory=list)

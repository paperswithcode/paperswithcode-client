from typing import Optional, List

from pydantic import Field

from tea_client.models import TeaClientModel


class ResultSyncRequest(TeaClientModel):
    """Evaluation table row object.

    Attributes:
        metrics (dict): Dictionary of metrics and metric values.
        methodology (str): Methodology used for this implementation.
        uses_additional_data (bool): Does this evaluation uses additional data
            not provided in the dataset used for other evaluations.
        paper (str, optional): Paper describing the evaluation.
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
    """

    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""


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
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
    """

    task: str
    dataset: str
    external_id: Optional[str] = ""
    metrics = List[MetricSyncRequest] = Field(default_factory=list)
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
    """

    id: str
    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""


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
        external_id (str, optional): Optional external ID used to identify rows
            when doing sync.
    """

    id: str
    task: str
    dataset: str
    external_id: Optional[str] = ""
    metrics = List[MetricSyncResponse] = Field(default_factory=list)
    results: List[ResultSyncResponse] = Field(default_factory=list)

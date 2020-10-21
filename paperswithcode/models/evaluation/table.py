from typing import List, Optional

from tea_client.models import TeaClientModel

from paperswithcode.models.page import Page


class EvaluationTable(TeaClientModel):
    """Evaluation table object.

    Attributes:
        id (str): Evaluation table ID.
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
    """

    id: str
    task: str
    dataset: str


class EvaluationTableCreateRequest(TeaClientModel):
    """Evaluation table create request object.

    Attributes:
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
    """

    task: str
    dataset: str


class EvaluationTableUpdateRequest(TeaClientModel):
    """Evaluation table update request object.

    Attributes:
        task (str): ID of the task used in evaluation.
        dataset (str): ID of the dataset used in evaluation.
    """

    task: Optional[str] = None
    dataset: Optional[str] = None


class EvaluationTables(Page):
    """Object representing a paginated page of evaluation tables.

    Attributes:
        count (int): Number of elements matching the query.
        next_page (int, optional): Number of the next page.
        previous_page (int, optional): Number of the previous page.
        results (List[SotaPartial]): List of evaluation tables on this page.
    """

    results: List[EvaluationTable]

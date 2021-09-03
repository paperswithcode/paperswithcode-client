from urllib import parse
from typing import Dict, Optional


from tea_client.http import HttpClient
from tea_client.handler import handler

from paperswithcode.config import config
from paperswithcode.models import (
    Paper,
    Papers,
    Repositories,
    Conference,
    Conferences,
    Proceeding,
    Proceedings,
    Area,
    Areas,
    Task,
    TaskCreateRequest,
    TaskUpdateRequest,
    Tasks,
    Dataset,
    DatasetCreateRequest,
    DatasetUpdateRequest,
    Datasets,
    Method,
    Methods,
    Metric,
    Metrics,
    MetricCreateRequest,
    MetricUpdateRequest,
    Result,
    Results,
    ResultCreateRequest,
    ResultUpdateRequest,
    EvaluationTable,
    EvaluationTables,
    EvaluationTableCreateRequest,
    EvaluationTableUpdateRequest,
    EvaluationTableSyncRequest,
    EvaluationTableSyncResponse,
)


class PapersWithCodeClient:
    """PapersWithCode client."""

    def __init__(self, token=None, url=None):
        url = url or config.server_url
        self.http = HttpClient(
            url=f"{url}/api/v{config.api_version}",
            token=token or "",
            authorization_method=HttpClient.Authorization.token,
        )

    @staticmethod
    def __params(page: int, items_per_page: int, **kwargs) -> Dict[str, str]:
        params = {key: str(value) for key, value in kwargs.items()}
        params["page"] = str(page)
        params["items_per_page"] = str(items_per_page)
        return params

    @staticmethod
    def __parse(url: str) -> int:
        """Return page number."""
        p = parse.urlparse(url)
        if p.query == "":
            return 1
        else:
            q = parse.parse_qs(p.query)
            return q.get("page", [1])[0]

    @classmethod
    def __page(cls, result, page_model):
        next_page = result["next"]
        if next_page is not None:
            next_page = cls.__parse(next_page)
        previous_page = result["previous"]
        if previous_page is not None:
            previous_page = cls.__parse(previous_page)
        return page_model(
            count=result["count"],
            next_page=next_page,
            previous_page=previous_page,
            results=result["results"],
        )

    @handler
    def paper_list(
        self,
        q: Optional[str] = None,
        arxiv_id: Optional[str] = None,
        title: Optional[str] = None,
        abstract: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a paginated list of papers.

        Args:
            q (str, optional): Filter papers by querying the paper title and
                abstract.
            arxiv_id (str, optional): Filter papers by arxiv id.
            title (str, optional): Filter papers by part of the title.
            abstract (str, optional): Filter papers by part of the abstract.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Papers: Papers object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if arxiv_id is not None:
            params["arxiv_id"] = arxiv_id
        if title is not None:
            params["title"] = title
        if abstract is not None:
            params["abstract"] = abstract
            timeout = 60
        return self.__page(
            self.http.get("/papers/", params=params, timeout=timeout), Papers
        )

    @handler
    def paper_get(self, paper_id: str) -> Paper:
        """Return a paper by it's ID.

        Args:
            paper_id (str): ID of the paper.

        Returns:
            Paper: Paper object.
        """
        return Paper(**self.http.get(f"/papers/{paper_id}/"))

    @handler
    def paper_dataset_list(
        self, paper_id: str, page: int = 1, items_per_page: int = 50
    ) -> Repositories:
        """Return a list of datasets mentioned in the paper..

        Args:
            paper_id (str): ID of the paper.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Datasets: Datasets object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/datasets/", params=params),
            Datasets,
        )

    @handler
    def paper_repository_list(
        self, paper_id: str, page: int = 1, items_per_page: int = 50
    ) -> Repositories:
        """Return a list of paper implementations.

        Args:
            paper_id (str): ID of the paper.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Repositories: Repositories object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/repositories/", params=params),
            Repositories,
        )

    @handler
    def paper_task_list(
        self, paper_id: str, page: int = 1, items_per_page: int = 50
    ) -> Tasks:
        """Return a list of tasks mentioned in the paper.

        Args:
            paper_id (str): ID of the paper.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/tasks/", params=params), Tasks
        )

    @handler
    def paper_method_list(
        self, paper_id: str, page: int = 1, items_per_page: int = 50
    ) -> Methods:
        """Return a list of methods mentioned in the paper.

        Args:
            paper_id (str): ID of the paper.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Methods: Methods object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/methods/", params=params),
            Methods,
        )

    @handler
    def paper_result_list(
        self, paper_id: str, page: int = 1, items_per_page: int = 50
    ) -> Results:
        """Return a list of evaluation results for the paper.

        Args:
            paper_id (str): ID of the paper.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Results: Results object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/results/", params=params),
            Results,
        )

    @handler
    def conference_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Conferences:
        """Return a paginated list of conferences.

        Args:
            q (str, optional): Search all searchable fields.
            name (str, optional): Filter conferences by part of the name.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Conferences: Conferences object.
        """
        params = self.__params(page, items_per_page)
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        return self.__page(
            self.http.get("/conferences/", params=params), Conferences
        )

    @handler
    def conference_get(self, conference_id: str) -> Conference:
        """Return a conference by it's ID.

        Args:
            conference_id (str): ID of the conference.

        Returns:
            Conference: Conference object.
        """
        return Conference(**self.http.get(f"/conferences/{conference_id}/"))

    @handler
    def proceeding_list(
        self, conference_id: str, page: int = 1, items_per_page: int = 50
    ) -> Proceedings:
        """Return a paginated list of conference proceedings.

        Args:
            conference_id (str): ID of the conference.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Proceedings: Proceedings object.
        """
        return self.__page(
            self.http.get(
                f"/conferences/{conference_id}/proceedings/",
                params=self.__params(page, items_per_page),
            ),
            Proceedings,
        )

    @handler
    def proceeding_get(
        self, conference_id: str, proceeding_id: str
    ) -> Proceeding:
        """Return a conference proceeding by it's ID.

        Args:
            conference_id (str): ID of the conference.
            proceeding_id (str): ID of the proceeding.

        Returns:
            Proceeding: Proceeding object.
        """
        return Proceeding(
            **self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}/"
            )
        )

    @handler
    def proceeding_paper_list(
        self,
        conference_id: str,
        proceeding_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a list of papers published in a confernce proceeding.

        Args:
            conference_id (str): ID of the conference.
            proceeding_id (str): ID of the proceding.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Papers: Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}"
                f"/papers/",
                params=params,
            ),
            Papers,
        )

    @handler
    def area_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Areas:
        """Return a paginated list of areas.

        Args:
            q (str, optional): Filter areas by querying the area name.
            name (str, optional): Filter areas by part of the name.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Areas: Areas object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name

        return self.__page(
            self.http.get("/areas/", params=params, timeout=timeout), Areas
        )

    @handler
    def area_get(self, area_id: str) -> Area:
        """Return an area by it's ID.

        Args:
            area_id (str): ID of the area.

        Returns:
            Area: Area object.
        """
        return Area(**self.http.get(f"/areas/{area_id}/"))

    @handler
    def area_task_list(
        self, area_id: str, page: int = 1, items_per_page: int = 50
    ) -> Tasks:
        """Return a paginated list of tasks in an area.

        Args:
            area_id (str): ID of the area.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/areas/{area_id}/tasks/", params=params), Tasks
        )

    @handler
    def task_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a paginated list of tasks.

        Args:
            q (str, optional): Filter tasks by querying the task name.
            name (str, optional): Filter tasks by part of th name.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        return self.__page(
            self.http.get("/tasks/", params=params, timeout=timeout), Tasks
        )

    @handler
    def task_get(self, task_id: str) -> Task:
        """Return a task by it's ID.

        Args:
            task_id (str): ID of the task.

        Returns:
            Task: Task object.
        """
        return Task(**self.http.get(f"/tasks/{task_id}/"))

    @handler
    def task_add(self, task: TaskCreateRequest) -> Task:
        """Add a task.

        Args:
           task (TaskCreateRequest): Task create request.

        Returns:
            Task: Created task.
        """
        return Task(**self.http.post("/tasks/", data=task))

    @handler
    def task_update(self, task_id: str, task: TaskUpdateRequest) -> Task:
        """Update a task.

        Args:
            task_id (str): ID of the task.
            task (TaskUpdateRequest): Task update request.

        Returns:
            Task: Updated task.
        """
        return Task(**self.http.patch(f"/tasks/{task_id}/", data=task))

    @handler
    def task_delete(self, task_id: str):
        """Delete a task.

        Args:
            task_id (str): ID of the task.
        """
        self.http.delete(f"/tasks/{task_id}/")

    @handler
    def task_parent_list(
        self, task_id: str, page: int = 1, items_per_page: int = 50
    ) -> Tasks:
        """Return a paginated list of parent tasks for a selected task.

        Args:
            task_id (str): ID of the task.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/parents/", params=params), Tasks
        )

    @handler
    def task_child_list(
        self, task_id: str, page: int = 1, items_per_page: int = 50
    ) -> Tasks:
        """Return a paginated list of child tasks for a selected task.

        Args:
            task_id (str): ID of the task.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/children/", params=params), Tasks
        )

    @handler
    def task_paper_list(
        self, task_id: str, page: int = 1, items_per_page: int = 50
    ) -> Papers:
        """Return a paginated list of papers for a selected task.

        Args:
            task_id (str): ID of the task.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Papers: Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/papers/", params=params), Papers
        )

    @handler
    def task_evaluation_list(
        self, task_id: str, page: int = 1, items_per_page: int = 50
    ) -> EvaluationTables:
        """Return a list of evaluation tables for a selected task.

        Args:
            task_id (str): ID of the task.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            EvaluationTables: EvaluationTables object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/evaluations/", params=params),
            EvaluationTables,
        )

    @handler
    def dataset_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        full_name: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Datasets:
        """Return a paginated list of datasets.

        Args:
            q (str, optional): Filter datasets by querying the dataset name.
            name (str, optional): Filter datasets by their name.
            full_name (str, optional): Filter datasets by their full name.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Datasets: Datasets object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if full_name is not None:
            params["full_name"] = full_name
        return self.__page(
            self.http.get("/datasets/", params=params, timeout=timeout),
            Datasets,
        )

    @handler
    def dataset_get(self, dataset_id: str) -> Dataset:
        """Return a dastaset by it's ID.

        Args:
            dataset_id (str): ID of the dataset.

        Returns:
            Dataset: Dataset object.
        """
        return Dataset(**self.http.get(f"/datasets/{dataset_id}/"))

    @handler
    def dataset_add(self, dataset: DatasetCreateRequest) -> Dataset:
        """Add a dataset.

        Args:
           dataset (DatasetCreateRequest): Dataset create request.

        Returns:
            Dataset: Created dataset.
        """
        return Dataset(**self.http.post("/datasets/", data=dataset))

    @handler
    def dataset_update(
        self, dataset_id: str, dataset: DatasetUpdateRequest
    ) -> Dataset:
        """Update a dataset.

        Args:
            dataset_id (str): ID of the dataset.
            dataset (DatasetUpdateRequest): Dataset update request.

        Returns:
            Dataset: Updated dataset.
        """
        return Dataset(
            **self.http.patch(f"/datasets/{dataset_id}/", data=dataset)
        )

    @handler
    def dataset_delete(self, dataset_id: str):
        """Delete a dataset.

        Args:
            dataset_id (str): ID of the dataset.
        """
        self.http.delete(f"/datasets/{dataset_id}/")

    @handler
    def dataset_evaluation_list(
        self, dataset_id: str, page: int = 1, items_per_page: int = 50
    ) -> EvaluationTables:
        """Return a list of evaluation tables for a selected dataset.

        Args:
            dataset_id (str): ID of the dasaset.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
           EvaluationTables: EvaluationTables object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(
                f"/datasets/{dataset_id}/evaluations/", params=params
            ),
            EvaluationTables,
        )

    @handler
    def method_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        full_name: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Methods:
        """Return a paginated list of methods.

        Args:
            q (str, optional): Search all searchable fields.
            name (str, optional): Filter methods by part of the name.
            full_name (str, optional): Filter methods by part of the full name.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Methods: Methods object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if full_name is not None:
            params["full_name"] = full_name
        return self.__page(
            self.http.get("/methods/", params=params, timeout=timeout),
            Methods,
        )

    @handler
    def method_get(self, method_id) -> Method:
        """Return a method by it's ID.

        Args:
            method_id (str): ID of the method.

        Returns:
            Method: Method object.
        """
        return Method(**self.http.get(f"/methods/{method_id}/"))

    @handler
    def evaluation_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> EvaluationTables:
        """Return a paginated list of evaluation tables.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            EvaluationTables: Evaluation table page object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get("/evaluations/", params=params), EvaluationTables
        )

    @handler
    def evaluation_get(self, evaluation_id: str) -> EvaluationTable:
        """Return a evaluation table by it's ID.

        Args:
            evaluation_id (str): ID of the evaluation table.

        Returns:
            EvaluationTable: Evaluation table object.
        """
        return EvaluationTable(
            **self.http.get(f"/evaluations/{evaluation_id}/")
        )

    @handler
    def evaluation_create(
        self, evaluation: EvaluationTableCreateRequest
    ) -> EvaluationTable:
        """Create an evaluation table.

        Args:
            evaluation (EvaluationTableCreateRequest): Evaluation table create
                request object.

        Returns:
            EvaluationTable: The new created evaluation table.
        """
        return EvaluationTable(
            **self.http.post("/evaluations/", data=evaluation)
        )

    @handler
    def evaluation_update(
        self, evaluation_id: str, evaluation: EvaluationTableUpdateRequest
    ) -> EvaluationTable:
        """Update an evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            evaluation (EvaluationTableUpdateRequest): Evaluation table update
                request object.

        Returns:
            EvaluationTable: The updated evaluation table.
        """
        return EvaluationTable(
            **self.http.patch(
                f"/evaluations/{evaluation_id}/", data=evaluation
            )
        )

    @handler
    def evaluation_delete(self, evaluation_id: str):
        """Delete an evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/")

    @handler
    def evaluation_metric_list(
        self, evaluation_id: str, page: int = 1, items_per_page: int = 50
    ) -> Metrics:
        """List all metrics used in the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Metrics: Metrics object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(
                f"/evaluations/{evaluation_id}/metrics/", params=params
            ),
            Metrics,
        )

    @handler
    def evaluation_metric_get(
        self, evaluation_id: str, metric_id: str
    ) -> Metric:
        """Get a metrics used in the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            metric_id (str): ID of the metric.

        Returns:
            Metric: Requested metric.
        """
        return Metric(
            **self.http.get(
                f"/evaluations/{evaluation_id}/metrics/{metric_id}/"
            )
        )

    @handler
    def evaluation_metric_add(
        self, evaluation_id: str, metric: MetricCreateRequest
    ) -> Metric:
        """Add a metrics to the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            metric (MetricCreateRequest): Metric create request.

        Returns:
            Metric: Created metric.
        """
        return Metric(
            **self.http.post(
                f"/evaluations/{evaluation_id}/metrics/", data=metric
            )
        )

    @handler
    def evaluation_metric_update(
        self, evaluation_id: str, metric_id: str, metric: MetricUpdateRequest
    ) -> Metric:
        """Update a metrics in the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            metric_id (str): ID of the metric.
            metric (MetricCreateRequest): Metric update request.

        Returns:
            Metric: Updated metric.
        """
        return Metric(
            **self.http.patch(
                f"/evaluations/{evaluation_id}/metrics/{metric_id}/",
                data=metric,
            )
        )

    @handler
    def evaluation_metric_delete(self, evaluation_id: str, metric_id: str):
        """Delete a metrics from the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            metric_id (str): ID of the metric.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/metrics/{metric_id}/")

    @handler
    def evaluation_result_list(
        self, evaluation_id: str, page: int = 1, items_per_page: int = 50
    ) -> Results:
        """List all results from the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Results: Results object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(
                f"/evaluations/{evaluation_id}/results/", params=params
            ),
            Results,
        )

    @handler
    def evaluation_result_get(
        self, evaluation_id: str, result_id: str
    ) -> Result:
        """Get a result from the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            result_id (str): ID of the result.

        Returns:
            Result: Requested result.
        """
        return Result(
            **self.http.get(
                f"/evaluations/{evaluation_id}/results/{result_id}/"
            )
        )

    @handler
    def evaluation_result_add(
        self, evaluation_id: str, result: ResultCreateRequest
    ) -> Result:
        """Add a result to the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            result (ResultCreateRequest): Result create request.

        Returns:
            Result: Created result.
        """
        return Result(
            **self.http.post(
                f"/evaluations/{evaluation_id}/results/", data=result
            )
        )

    @handler
    def evaluation_result_update(
        self, evaluation_id: str, result_id: str, result: ResultUpdateRequest
    ) -> Result:
        """Update a result in the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            result_id (str): ID of the result.
            result (ResultUpdateRequest): Result update request.

        Returns:
            Result: Updated result.
        """
        return Result(
            **self.http.patch(
                f"/evaluations/{evaluation_id}/results/{result_id}/",
                data=result,
            )
        )

    @handler
    def evaluation_result_delete(self, evaluation_id: str, result_id: str):
        """Delete a result from the evaluation table.

        Args:
            evaluation_id (str): ID of the evaluation table.
            result_id (str): ID of the result.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/results/{result_id}/")

    @handler
    def evaluation_synchronize(
        self, evaluation: EvaluationTableSyncRequest
    ) -> EvaluationTableSyncResponse:
        d = self.http.post("/rpc/evaluation-synchronize/", data=evaluation)
        d["results"] = [result for result in d["results"]]
        return EvaluationTableSyncResponse(**d)

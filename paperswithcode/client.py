from urllib import parse
from typing import Dict, List


from tea_client.http import HttpClient
from tea_client.handler import handler

from paperswithcode.config import config
from paperswithcode.models import (
    Paper,
    Papers,
    Repository,
    Conference,
    Conferences,
    Proceeding,
    Proceedings,
    Area,
    Areas,
    Task,
    Tasks,
    Dataset,
    Datasets,
    Method,
    Methods,
    Result,
    SotaPartial,
    SotaPartials,
    Sota,
)


class PapersWithCodeClient:
    """PapersWithCode client."""

    def __init__(self):
        self.http = HttpClient(
            url=f"{config.server_url}/api/v{config.api_version}"
        )

    @staticmethod
    def __params(page: int, items_per_page: int, **kwargs) -> Dict[str, str]:
        params = {key: str(value) for key, value in kwargs.items()}
        params.update(
            {"items_per_page": str(items_per_page), "page": str(page)}
        )
        return params

    @staticmethod
    def __parse(url: str) -> int:
        """Return page number."""
        p = parse.urlparse(url)
        if p.query == "":
            return 1
        else:
            q = parse.parse_qs(p.query)
            return q["page"][0]

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
    def paper_list(self, page: int = 1, items_per_page: int = 50) -> Papers:
        """Return a paginated list of papers.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Papers: Papers object.
        """
        return self.__page(
            self.http.get(
                "/papers/", params=self.__params(page, items_per_page),
            ),
            Papers,
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
    def paper_repository_list(self, paper_id: str) -> List[Repository]:
        """Return a list of paper implementations.

        Args:
            paper_id (str): ID of the paper.

        Returns:
            List[Repository]: List of repository objects.
        """
        return [
            Repository(**r)
            for r in self.http.get(f"/papers/{paper_id}/repositories/")
        ]

    @handler
    def paper_task_list(self, paper_id: str) -> List[Task]:
        """Return a list of tasks mentioned in the paper.

        Args:
            paper_id (str): ID of the paper.

        Returns:
            List[Task]: List of task objects.
        """
        return [Task(**t) for t in self.http.get(f"/papers/{paper_id}/tasks/")]

    @handler
    def paper_method_list(self, paper_id: str) -> List[Method]:
        """Return a list of methods mentioned in the paper.

        Args:
            paper_id (str): ID of the paper.

        Returns:
            List[Method]: List of method objects.
        """
        return [
            Method(**t) for t in self.http.get(f"/papers/{paper_id}/methods/")
        ]

    @handler
    def paper_result_list(self, paper_id: str) -> List[Result]:
        """Return a list of evaluation results for the paper.

        Args:
            paper_id (str): ID of the paper.

        Returns:
            List[Result]: List of result objects.
        """
        return [
            Result(**t) for t in self.http.get(f"/papers/{paper_id}/results/")
        ]

    @handler
    def conference_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> Conferences:
        """Return a paginated list of conferences.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Conferences: Conferences object.
        """
        return self.__page(
            self.http.get(
                "/conferences/", params=self.__params(page, items_per_page)
            ),
            Conferences,
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
        self, conference_id: str, proceeding_id: str
    ) -> List[Paper]:
        """Return a list of papers published in a confernce proceeding.

        Args:
            conference_id (str): ID of the conference.
            proceeding_id (str): ID of the proceding.

        Returns:
            List[Paper]: List of paper objects.
        """
        return [
            Paper(**p)
            for p in self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}"
                f"/papers/"
            )
        ]

    @handler
    def area_list(self, page: int = 1, items_per_page: int = 50) -> Areas:
        """Return a paginated list of areas.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Areas: Areas object.
        """
        return self.__page(
            self.http.get(
                "/areas/", params=self.__params(page, items_per_page)
            ),
            Areas,
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
        return self.__page(
            self.http.get(
                f"/areas/{area_id}/tasks/",
                params=self.__params(page, items_per_page),
            ),
            Tasks,
        )

    @handler
    def task_list(self, page: int = 1, items_per_page: int = 50) -> Tasks:
        """Return a paginated list of tasks.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Tasks: Tasks object.
        """
        return self.__page(
            self.http.get(
                "/tasks/", params=self.__params(page, items_per_page)
            ),
            Tasks,
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
        return self.__page(
            self.http.get(
                f"/tasks/{task_id}/papers/",
                params=self.__params(page, items_per_page),
            ),
            Papers,
        )

    @handler
    def task_sota_list(self, task_id: str) -> List[SotaPartial]:
        """Return a list of evaluation tables for a selected task.

        Args:
            task_id (str): ID of the task.

        Returns:
            List[SotaPartial]: List of short evaluation table objects.
        """
        return [
            SotaPartial(**sp)
            for sp in self.http.get(f"/tasks/{task_id}/sota/")
        ]

    @handler
    def dataset_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> Datasets:
        """Return a paginated list of datasets.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Datasets: Datasets object.
        """
        return self.__page(
            self.http.get(
                "/datasets/", params=self.__params(page, items_per_page)
            ),
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
    def dataset_sota_list(self, dataset_id: str) -> List[SotaPartial]:
        """Return a list of evaluation tables for a selected dataset.

        Args:
            dataset_id (str): ID of the dasaset.

        Returns:
            List[SotaPartial]: List of short evaluation table objects.
        """
        return [
            SotaPartial(**sp)
            for sp in self.http.get(f"/datasets/{dataset_id}/sota/")
        ]

    @handler
    def method_list(self, page: int = 1, items_per_page: int = 50) -> Methods:
        """Return a paginated list of methods.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            Methods: Methods object.
        """
        return self.__page(
            self.http.get(
                "/methods/", params=self.__params(page, items_per_page)
            ),
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
    def sota_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> SotaPartials:
        """Return a paginated list of evaluation tables.

        Args:
            page (int): Desired page.
            items_per_page (int): Desired number of items per page.
                Default: 50.

        Returns:
            SotaPartials: Evaluation table page object.
        """
        return self.__page(
            self.http.get(
                "/sota/", params=self.__params(page, items_per_page)
            ),
            SotaPartials,
        )

    @handler
    def sota_get(self, sota_id: str) -> Sota:
        """Return a evaluation table by it's ID.

        Args:
            sota_id (str): ID of the evaluation table.

        Returns:
            Sota: Evaluation table object.
        """
        return Sota(**self.http.get(f"/sota/{sota_id}/"))

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
        return self.__page(
            self.http.get(
                "/papers/", params=self.__params(page, items_per_page),
            ),
            Papers,
        )

    @handler
    def paper_get(self, paper_id: str) -> Paper:
        return Paper(**self.http.get(f"/papers/{paper_id}/"))

    @handler
    def paper_repository_list(self, paper_id: str) -> List[Repository]:
        return [
            Repository(**r)
            for r in self.http.get(f"/papers/{paper_id}/repositories/")
        ]

    @handler
    def conference_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> Conferences:
        return self.__page(
            self.http.get(
                "/conferences/", params=self.__params(page, items_per_page)
            ),
            Conferences,
        )

    @handler
    def conference_get(self, conference_id: str) -> Conference:
        return Conference(**self.http.get(f"/conferences/{conference_id}/"))

    @handler
    def proceeding_list(self, conference_id: str) -> Proceedings:
        return self.__page(
            self.http.get(f"/conferences/{conference_id}/proceedings/"),
            Proceedings,
        )

    @handler
    def proceeding_get(
        self, conference_id: str, proceeding_id: str
    ) -> Proceeding:
        return Proceeding(
            **self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}/"
            )
        )

    @handler
    def proceeding_paper_list(
        self, conference_id: str, proceeding_id: str
    ) -> List[Paper]:
        return [
            Paper(**p)
            for p in self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}"
                f"/papers/"
            )
        ]

    @handler
    def area_list(self, page: int = 1, items_per_page: int = 50) -> Areas:
        return self.__page(
            self.http.get(
                "/areas/", params=self.__params(page, items_per_page)
            ),
            Areas,
        )

    @handler
    def area_get(self, area_id: str) -> Area:
        return Area(**self.http.get(f"/areas/{area_id}/"))

    @handler
    def area_task_list(
        self, area_id: str, page: int = 1, items_per_page: int = 50
    ) -> Tasks:
        return self.__page(
            self.http.get(
                f"/areas/{area_id}/tasks/",
                params=self.__params(page, items_per_page),
            ),
            Tasks,
        )

    @handler
    def task_list(self, page: int = 1, items_per_page: int = 50) -> Tasks:
        return self.__page(
            self.http.get(
                "/tasks/", params=self.__params(page, items_per_page)
            ),
            Tasks,
        )

    @handler
    def task_get(self, task_id: str) -> Task:
        return Task(**self.http.get(f"/tasks/{task_id}/"))

    @handler
    def task_paper_list(
        self, task_id: str, page: int = 1, items_per_page: int = 50
    ) -> Papers:
        return self.__page(
            self.http.get(
                f"/tasks/{task_id}/papers/",
                params=self.__params(page, items_per_page),
            ),
            Papers,
        )

    @handler
    def task_sota_list(self, task_id: str) -> List[SotaPartial]:
        return [
            SotaPartial(**sp)
            for sp in self.http.get(f"/tasks/{task_id}/sota/")
        ]

    @handler
    def dataset_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> Datasets:
        return self.__page(
            self.http.get(
                "/datasets/", params=self.__params(page, items_per_page)
            ),
            Datasets,
        )

    @handler
    def dataset_get(self, dataset_id: str) -> Dataset:
        return Dataset(**self.http.get(f"/datasets/{dataset_id}/"))

    @handler
    def dataset_sota_list(self, dataset_id: str) -> List[SotaPartial]:
        return [
            SotaPartial(**sp)
            for sp in self.http.get(f"/datasets/{dataset_id}/sota/")
        ]

    @handler
    def method_list(self, page: int = 1, items_per_page: int = 50) -> Methods:
        return self.__page(
            self.http.get(
                "/methods/", params=self.__params(page, items_per_page)
            ),
            Methods,
        )

    @handler
    def method_get(self, method_id) -> Method:
        return Method(**self.http.get(f"/methods/{method_id}/"))

    @handler
    def sota_list(
        self, page: int = 1, items_per_page: int = 50
    ) -> SotaPartials:
        return self.__page(
            self.http.get(
                "/sota/", params=self.__params(page, items_per_page)
            ),
            SotaPartials,
        )

    @handler
    def sota_get(self, sota_id: str) -> Sota:
        return Sota(**self.http.get(f"/sota/{sota_id}/"))

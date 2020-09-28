from typing import Optional

from tea_client.models import TeaClientModel


class Page(TeaClientModel):
    count: int
    next_page: Optional[int]
    previous_page: Optional[int]

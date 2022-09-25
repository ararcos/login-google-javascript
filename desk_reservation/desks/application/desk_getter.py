from typing import Optional

from ..domain import Desk
from ..domain.services.desk_service import DeskService


class FinderById:
    def __init__(self, desk_service: DeskService):
        self.desk_service = desk_service

    def execute(self, desk_id: str) -> Optional[Desk]:
        return self.desk_service.get(desk_id)

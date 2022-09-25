from ..domain import Desk
from ..domain.services.desk_service import DeskService


class DeskUpdater:
    def __init__(self, desk_service: DeskService):
        self.desk_service = desk_service

    def execute(self, user_id: str, desk: Desk) -> Desk:
        return self.desk_service.update(user_id, desk)

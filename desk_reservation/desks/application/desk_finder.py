from typing import List


from ..domain import Desk
from ..domain.services.desk_service import DeskService
from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria


class DeskFinder:
    def __init__(self, desk_service: DeskService):
        self.desk_service = desk_service

    def execute(self, criteria: Criteria) -> List[Desk]:
        return self.desk_service.find(criteria)

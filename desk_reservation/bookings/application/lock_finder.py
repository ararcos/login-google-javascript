from typing import List

from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..domain.entities import LockBooking
from ..domain.services import LockService


class LockFinder:
    def __init__(self, lock_service: LockService):
        self.lock_service = lock_service
    def execute(self, criteria: Criteria) -> List[LockBooking]:
        return self.lock_service.find(criteria)

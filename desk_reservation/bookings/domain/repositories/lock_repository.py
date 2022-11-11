from abc import ABC, abstractmethod
from typing import List

from desk_reservation.shared.infrastructure.firestore.firestore_criteria.criteria import (
    Criteria,
)
from ..entities import LockBooking


class LockRepository(ABC):
    @abstractmethod
    def create(self, lock_booking: LockBooking) -> LockBooking:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[LockBooking]:
        pass

    @abstractmethod
    def delete(self, lock_id: str, user_id: str) -> bool:
        pass

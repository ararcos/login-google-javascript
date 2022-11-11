import typing

from ..entities import LockBooking
from ..repositories import LockRepository
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.infrastructure.firestore.firestore_criteria import (
    Criteria,
)


class LockService:
    def __init__(self, lock_repository: LockRepository):
        self.lock_repository = lock_repository

    def create(self, lock_booking: LockBooking) -> LockBooking:
        return self.lock_repository.create(lock_booking)

    def find(self, criteria: Criteria) -> typing.List[LockBooking]:
        return self.lock_repository.find(criteria)

    def delete(self, booking_id: str, user_id: str) -> bool:
        result = self.lock_repository.delete(booking_id, user_id)
        if not result:
            raise IdNotFoundError("Lock Booking", booking_id)
        return result

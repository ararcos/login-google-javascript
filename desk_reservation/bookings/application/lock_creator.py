from ..domain.services import LockService
from ...bookings.domain.entities import LockBooking


class LockCreator:
    def __init__(self, lock_service: LockService):
        self.lock_service = lock_service

    def execute(self, lock_booking: LockBooking) -> LockBooking:
        return self.lock_service.create(lock_booking)

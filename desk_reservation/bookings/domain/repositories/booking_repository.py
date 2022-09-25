from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import SeatBooking
from desk_reservation.shared.infrastructure.firestore.firestore_criteria.criteria import Criteria


class BookingRepository(ABC):
    @abstractmethod
    def create(self, booking: SeatBooking) -> SeatBooking:
        pass

    @abstractmethod
    def create_many(self, bookings: List[SeatBooking]) -> List[SeatBooking]:
        pass

    @abstractmethod
    def get(self, booking_id: str) -> Optional[SeatBooking]:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[SeatBooking]:
        pass

    @abstractmethod
    def update(self, booking_id: str, updated_by: str, booking: SeatBooking) -> Optional[SeatBooking]:
        pass

    @abstractmethod
    def delete(self, booking_id: str, user_id:str) -> bool:
        pass

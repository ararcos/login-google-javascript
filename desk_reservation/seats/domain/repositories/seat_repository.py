from abc import ABC, abstractmethod
from typing import Optional, List

from desk_reservation.shared.infrastructure.firestore.firestore_criteria import Criteria
from ..entities.seat import Seat


class SeatRepository(ABC):
    @abstractmethod
    def get(self, seat_id: str) -> Optional[Seat]:
        pass
    
    @abstractmethod
    def find(self, criteria: Criteria) -> List[Seat]:
        pass

    @abstractmethod
    def update(self, seat: Seat) -> Optional[Seat]:
        pass

    @abstractmethod
    def create(self, seat: Seat) -> Seat:
        pass

    @abstractmethod
    def create_many(self, seats: List[Seat]) -> List[Seat]:
        pass

    @abstractmethod
    def delete(self, seat_id: str) -> bool:
        pass

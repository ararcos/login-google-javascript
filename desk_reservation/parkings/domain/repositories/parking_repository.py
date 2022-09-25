from typing import List, Optional
from abc import ABC, abstractmethod

from ....shared.infrastructure.firestore.firestore_criteria import Criteria
from ..entities.parking import Parking


# pylint: disable=R0801
class ParkingRepository(ABC):
    @abstractmethod
    def get(self, parking_id: str) -> Optional[Parking]:
        pass

    @abstractmethod
    def create(self, parking: Parking) -> Parking:
        pass

    @abstractmethod
    def update(self, parking: Parking) -> Optional[Parking]:
        pass

    @abstractmethod
    def delete(self, parking_id: str) -> bool:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[Parking]:
        pass

from abc import ABC, abstractmethod
from typing import List, Optional

from ....shared.infrastructure import Criteria
from ..entities.ride import Ride, RideBooking


class RideRepository(ABC):

    @abstractmethod
    def create(self, ride: Ride) -> Ride:
        pass

    @abstractmethod
    def find_by_id(self, ride_id: str) -> Optional[Ride]:
        pass

    @abstractmethod
    def find_all(self, criteria: Criteria) -> List[Ride]:
        pass

    @abstractmethod
    def update(self, user_id: str, ride_id:str, ride: Ride) -> Optional[Ride]:
        pass

    @abstractmethod
    def delete(self, ride_id: str) -> bool:
        pass

    @abstractmethod
    def booking_ride(self, ride_booking: RideBooking) -> Optional[RideBooking]:
        pass

    @abstractmethod
    def find_booking_ride(self, criteria: Criteria) -> List[RideBooking]:
        pass

    @abstractmethod
    def find_by_id_booking_ride(self, ride_booking_id: str) -> Optional[RideBooking]:
        pass

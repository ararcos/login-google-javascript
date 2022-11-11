from datetime import date
from typing import List, Optional

from ....shared.domain.exceptions import BadRequestError, PermissionsError
from ....shared.infrastructure import Criteria
from ....users.domain import UserRepository, User
from ...domain.entities.ride import Ride, RideBooking
from ..repositories.ride_repository import RideRepository


class RideService:
    def __init__(self, ride_repository: RideRepository, user_repository: UserRepository):
        self.ride_repository = ride_repository
        self.user_repository = user_repository

    def ride_is_old(self, ride: Ride) -> bool:
        if ride.ride_date.date() < date.today():
            return True
        return False

    def user_is_driver_of_ride(self, user_id: str, offerer_user_id: str) -> bool:
        if user_id == offerer_user_id:
            return True
        return False

    def create(self, ride: Ride) -> Ride:
        if self.ride_is_old(ride):
            raise BadRequestError("Ride is old")
        return self.ride_repository.create(ride)

    def find_by_id(self, ride_id: str) -> Optional[Ride]:
        ride = self.ride_repository.find_by_id(ride_id)
        if ride:
            ride.passengers = self.populate_booking_ride(ride.passengers)
        return ride

    def find_all(self, criteria: Criteria) -> List[Ride]:
        rides = self.ride_repository.find_all(criteria)
        for ride in rides:
            ride.passengers = self.populate_booking_ride(ride.passengers)
        return rides

    def update(self, user_id: str, ride_id: str, ride: Ride) -> Optional[Ride]:
        if self.ride_is_old(ride):
            raise BadRequestError("Ride is old")
        if self.user_is_driver_of_ride(user_id, ride.offerer_user_id):
            return self.ride_repository.update(user_id=user_id, ride_id=ride_id, ride=ride)
        raise PermissionsError("User is not driver of ride")

    def delete(self, user_id: str, ride_id: str) -> bool:
        ride = self.ride_repository.find_by_id(ride_id)
        if self.user_is_driver_of_ride(user_id, ride.offerer_user_id):
            return self.ride_repository.delete(ride_id)
        raise PermissionsError("User is not driver of ride")

    def delete_booking_ride(self, ride_id: str, ride_booking_ids: List[str]) -> bool:
        ride = self.ride_repository.find_by_id(ride_id)
        if ride:
            new_passengers = [id for id in ride.passengers if id not in ride_booking_ids]
            for id in ride_booking_ids:
                doc_ref = self.ride_repository.delete_booking_ride(id)
            ride.passengers = new_passengers
            self.ride_repository.update(user_id=ride.offerer_user_id, ride_id=ride_id, ride=ride)
            return True
        return False

    def booking_ride(self, ride_booking: RideBooking, ride: Ride) -> Optional[RideBooking]:
        if len(ride.passengers) < ride.total_spots:
            return self.ride_repository.booking_ride(ride_booking)
        raise BadRequestError("Ride is full")

    def populate_booking_ride(self, passengers_ids: List[str]) -> List[dict]:
        passengers = []
        for passenger_id in passengers_ids:
            passenger = self.ride_repository.find_by_id_booking_ride(passenger_id)
            if passenger:
                passengers.append(passenger.__dict__)
        return passengers
    
    def find_booking_ride(self, criteria: Criteria) -> List[RideBooking]:
        return self.ride_repository.find_booking_ride(criteria)

    def populate_user_info(self, offerer_user_id: str) -> User:
        user = self.user_repository.get(offerer_user_id)
        return user

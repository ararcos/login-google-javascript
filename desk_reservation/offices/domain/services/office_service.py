from typing import List, Optional, Tuple

from ..entities.office import Office
from ..repositories.office_repository import OfficeRepository
from ....shared.infrastructure import Criteria
from ....shared.domain.exceptions import PermissionsError
from ....seats.domain import SeatRepository, Seat
from ....parkings.domain import ParkingRepository, Parking
from ....users.domain import UserRepository


class OfficeService:
    def __init__(
        self,
        seat_repository: SeatRepository,
        parking_repository: ParkingRepository,
        office_repository: OfficeRepository,
        user_repository: UserRepository
    ):
        self.seat_repository = seat_repository
        self.parking_repository = parking_repository
        self.office_repository = office_repository
        self.user_repository = user_repository

    def create(self, office: Office, user_id: str) -> Office:
        if self._has_permissions(user_id, office.office_id):
            return self.office_repository.create(office)
        raise PermissionsError("Create an office")

    def update(self, office_id: str, office: Office,  user_id: str) -> Optional[Office]:
        if self._has_permissions(user_id, office.office_id):
            return self.office_repository.update(
                office_id=office_id, office=office
            )
        raise PermissionsError("Update an office")

    def delete(self, office_id: str, user_id: str) -> bool:
        office = self.office_repository.get(office_id=office_id)
        if self._has_permissions(user_id, office.office_id):
            return self.office_repository.delete(office_id=office_id)
        raise PermissionsError("Delete an office")

    def get(self, office_id: str) -> Optional[Office]:
        office = self.office_repository.get(office_id=office_id)
        if office:
            seats, parkings = self._populate_office(
                seats_ids=office.seats, parkings_ids=office.parkings)
            office.seats = seats
            office.parkings = parkings

        return office

    def find(self, criteria: Criteria) -> List[Office]:
        offices = self.office_repository.find(criteria=criteria)
        if len(offices) > 0:
            for office in offices:
                seats, parkings = self._populate_office(
                    seats_ids=office.seats, parkings_ids=office.parkings)
                office.seats = seats
                office.parkings = parkings

        return offices

    def _populate_office(
        self,
        seats_ids: List[str],
        parkings_ids: List[str]
    ) -> Tuple[List[Seat], List[Parking]]:

        parkings = []
        seats = []

        for parking_id in parkings_ids:
            parking = self.parking_repository.get(parking_id=parking_id)
            if parking:
                parkings.append(parking)

        for seat_id in seats_ids:
            seat = self.seat_repository.get(seat_id=seat_id)
            if seat:
                seats.append(seat)

        return (seats, parkings)

    def _has_permissions(self, user_id: str, office_id: str) -> bool:
        user = self.user_repository.get(google_id=user_id)
        office = self.office_repository.get(office_id=office_id)
        is_admin = user.admin if user else False
        is_manager = user_id in office.managers if office else False

        return is_admin or is_manager

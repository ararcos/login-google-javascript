from typing import Optional, List

from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.domain.exceptions import NameAlreadyExistsError
from ....shared.infrastructure.firestore.firestore_criteria.operator import Operator
from ....offices.domain.entities.office import Office
from ....offices.domain.repositories.office_repository import OfficeRepository
from ..entities.seat import Seat
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..repositories.seat_repository import SeatRepository
from ....users.domain.repositories.user_repository import UserRepository


class SeatService:
    def __init__(
        self,
        user_repository: UserRepository,
        seat_repository: SeatRepository,
        office_repository: OfficeRepository,
    ):
        self.user_repository = user_repository
        self.seat_repository = seat_repository
        self.office_repository = office_repository

    def create_seat(self, user_id: str, seat: Seat) -> Seat:
        if not self.user_is_admin_or_manager(user_id=user_id, office_id=seat.office_id):
            raise PermissionsError("You must be an admin or a manager.")
        if self.is_seat_name_repeated_in_same_office(name=seat.name, office_id=seat.office_id):
            raise NameAlreadyExistsError('Seat', seat.name)

        return self.seat_repository.create(seat)

    def delete_seat(self, user_id: str, office_id: str, seat_id: str) -> bool:
        if not self.user_is_admin_or_manager(user_id=user_id, office_id=office_id):
            raise PermissionsError("You must be an admin or a manager.")
        result = self.seat_repository.delete(seat_id=seat_id)
        if not result:
            raise IdNotFoundError("Seat", seat_id)
        return result

    def delete_many_seats(self, seats: List[str]) -> List[str]:
        result: List[str] = []
        for seat_id in seats:
            if self.seat_repository.delete(seat_id):
                result.append(seat_id)
        return result

    def update_seat(self, user_id: str, seat: Seat) -> Optional[Seat]:
        if not self.user_is_admin_or_manager(user_id=user_id, office_id=seat.office_id):
            raise PermissionsError("You must be an admin or a manager.")
        if self.is_seat_name_repeated_in_same_office(name=seat.name, office_id=seat.office_id):
            raise NameAlreadyExistsError('Seat', seat.name)
        result = self.seat_repository.update(seat=seat)
        if not result:
            raise IdNotFoundError("Seat", seat.seat_id)
        return result

    def get_seat_by_id(self, seat_id: str) -> Optional[Seat]:
        result = self.seat_repository.get(seat_id)
        if not result:
            raise IdNotFoundError("Seat", seat_id)
        return result

    def find_seats(self, criteria: Criteria) -> List[Seat]:
        return self.seat_repository.find(criteria)

    def user_is_admin(self, user_id: str) -> bool:
        user = self.user_repository.get(google_id=user_id)
        if not (user and user.admin):
            return False
        return True

    def user_is_manager(self, user_id: str, office_id: str) -> bool:
        office: Optional[Office] = self.office_repository.get(office_id)
        if not office or user_id not in office.managers:
            return False
        return True

    def user_is_admin_or_manager(self, user_id: str, office_id: str) -> bool:
        is_manager = self.user_is_manager(user_id=user_id, office_id=office_id)
        is_admin = self.user_is_admin(user_id=user_id)
        if not (is_manager or is_admin):
            return False
        return True

    def is_seat_name_repeated_in_same_office(self, name: str, office_id: str) -> bool:
        criteria_to_find_repeated_names = Criteria(
            filters=[
                Filter(
                    field='name',
                    operator=Operator.EQUAL,
                    value=name
                ),
                Filter(
                    field='office_id',
                    operator=Operator.EQUAL,
                    value=office_id
                )
            ]
        )
        find_result = self.find_seats(criteria_to_find_repeated_names)
        return len(find_result) > 0

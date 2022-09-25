from datetime import datetime
from typing import List, Optional

from ..entities.desk import Desk
from ..repositories.desk_repository import DeskRepository
from ..exceptions.too_many_seats_error import TooManySeatsError
from ....offices.domain.entities.office import Office
from ....offices.domain.repositories.office_repository import OfficeRepository
from ....seats.domain.repositories.seat_repository import SeatRepository
from ....users.domain.repositories import UserRepository
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.domain.exceptions.name_already_exists_error import (
    NameAlreadyExistsError,
)


class DeskService:
    def __init__(
        self,
        desk_repository: DeskRepository,
        user_repository: UserRepository,
        office_repository: OfficeRepository,
        seat_repository: SeatRepository,
    ):
        self.desk_repository = desk_repository
        self.user_repository = user_repository
        self.office_repository = office_repository
        self.seat_repository = seat_repository

    def create(self, user_id: str, desk: Desk) -> Desk:
        office_result = self.office_repository.get(desk.office_id)

        if not self.has_permissions(user_id=user_id, office=office_result):
            raise PermissionsError("Create a Desk")

        self.desk_seats_list_len_validator(desk)
        self.names_desk_validator(desk, office_result)

        return self.desk_repository.create(desk)

    def update(self, user_id: str, desk: Desk) -> Desk:
        office_result = self.office_repository.get(desk.office_id)

        if not self.has_permissions(user_id, office_result):
            raise PermissionsError("Update a Desk")
        self.desk_seats_list_len_validator(desk)
        self.names_desk_validator(desk, office_result)

        return self.desk_repository.update(user_id, desk)

    def delete(self, desk: Desk, user_id: str) -> bool:
        office_result = self.office_repository.get(desk.office_id)

        if not self.has_permissions(user_id=user_id, office=office_result):
            raise PermissionsError("Delete a Desk")
        desk.deleted_at = datetime.today()
        desk.deleted_by = user_id

        return self.desk_repository.delete(user_id=user_id, desk_id=desk.desk_id)

    def get(self, desk_id: str) -> Optional[Desk]:
        desk = self.desk_repository.get(desk_id)
        return desk

    def find(self, criteria: Criteria) -> List[Desk]:
        desks = self.desk_repository.find(criteria)
        return desks

    def has_permissions(self, user_id: str, office: Office) -> bool:
        user = self.user_repository.get(google_id=user_id)
        entities_exist = hasattr(user, "admin") and hasattr(office, "managers")
        return entities_exist and (user.admin or user_id in office.managers)

    def names_desk_validator(self, desk: Desk, office: Office) -> bool:
        if desk.desk_name in office.desks:
            raise NameAlreadyExistsError("Desk", desk.desk_name)
        return True

    def desk_seats_list_len_validator(self, desk: Desk) -> bool:
        if len(desk.seats_list) > 12:
            raise TooManySeatsError("Desk")
        return True

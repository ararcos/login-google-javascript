from typing import List, Optional

from ....offices.domain.entities.office import Office
from ..entities.parking import Parking
from ....shared.domain.exceptions import IdNotFoundError
from ....shared.domain.exceptions import NameAlreadyExistsError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.infrastructure.firestore.firestore_criteria.operator import Operator
from ....users.domain.repositories import UserRepository
from ....offices.domain.repositories.office_repository import OfficeRepository
from ..repositories import ParkingRepository
from ....users.domain.entities.user import User


class ParkingService:

    def __init__(
    self,
    parking_repository: ParkingRepository,
    user_repository: UserRepository,
    office_repository: OfficeRepository
    ):
        self.parking_repository = parking_repository
        self.user_repository = user_repository
        self.office_repository = office_repository
        
    def create_parking(self, user_id: str, parking: Parking) -> Parking:
        
        if not self.has_permissions(user_id=user_id, office_id=parking.office_id):
            raise PermissionsError("You must be an admin or a manager.")
        if self.is_parking_name_repeated_in_same_office(name=parking.name, office_id=parking.office_id):
            raise NameAlreadyExistsError('Parking', parking.name)

        return self.parking_repository.create(parking)

    def delete_parking(self, user_id: str, office_id: str, parking_id: str) -> bool:
        if not self.has_permissions(user_id=user_id, office_id=office_id):
            raise PermissionsError("You must be an admin or a manager.")
        result = self.parking_repository.delete(parking_id=parking_id)
        if not result:
            raise IdNotFoundError("Parking", parking_id)
        return result

    def find_parkings(self, criteria: Criteria) -> List[Parking]:
        return self.parking_repository.find(criteria)
    
    def update_parking(self, user_id: str, parking: Parking) -> Parking:
        if not self.has_permissions(user_id=user_id, office_id=parking.office_id):
            raise PermissionsError("You must be an admin or a manager.")
        if self.is_parking_name_repeated_in_same_office(name=parking.name, office_id=parking.office_id):
            raise NameAlreadyExistsError('Parking', parking.name)
        result = self.parking_repository.update(parking=parking)
        if not result:
            raise IdNotFoundError("Parking", parking.parking_id)
        return result
    
    def get_parking_by_id(self, parking_id: str) -> Parking:
        result = self.parking_repository.get(parking_id)
        if not result:
            raise IdNotFoundError("Parking", parking_id)
        return result
    
    def has_permissions(self, user_id: str, office_id: str) -> bool:
        is_admin = self.user_is_admin(user_id)
        is_manager = self.user_is_manager(user_id, office_id)
        if is_admin or is_manager:
            return True
        return False

    def user_is_admin(self, user_id: str) -> bool:
        user: Optional[User] = self.user_repository.get(google_id=user_id)
        if not user or not user.admin:
            return False
        return True

    def user_is_manager(self, user_id: str, office_id: str) -> bool:
        office: Optional[Office] = self.office_repository.get(
            office_id=office_id)
        if not office or user_id not in office.managers:
            return False
        return True

    def is_parking_name_repeated_in_same_office(self, name: str, office_id: str)-> bool:
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
        find_result = self.find_parkings(criteria_to_find_repeated_names)
        return len(find_result)>0
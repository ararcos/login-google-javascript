from typing import List

from ...shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..domain.services.user_service import UserService
from ..domain import User


class UserFinder:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, criteria: Criteria) -> List[User]:
        return self.user_service.find_users(criteria)

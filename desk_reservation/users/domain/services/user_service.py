from typing import List, Optional

from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..exceptions.incorrect_domain_error import IncorrectDomainError
from ..repositories.user_repository import UserRepository
from ..entities import User


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, google_id: str) -> Optional[User]:
        user_find: Optional[User] = self.user_repository.get(
            google_id=google_id)
        return user_find

    def find_users(self, criteria: Criteria) -> List[User]:
        return self.user_repository.find(criteria)

    def create_user(self, user_id: str, user: User) -> User:
        if not self.is_admin(user_id):
            raise PermissionsError('Create a User')
        if self.correct_domain(user) is False:
            raise IncorrectDomainError()
        return self.user_repository.create(user)

    def edit_user(self, user_id: str, user: User) -> Optional[User]:
        user_editor = self.user_repository.get(user_id)
        if (user.google_id != user_id) or user_editor.admin is False:
            raise PermissionsError('Update a User')
        return self.user_repository.edit(
            google_id=user_id,
            user=user
        )

    def delete_user(self, google_id: str, user_id: str) -> bool:
        if self.is_admin(google_id) is False:
            raise PermissionsError('Delete a User')
        return self.user_repository.delete(google_id=user_id)

    def is_admin(self, google_id: str) -> bool:
        user = self.user_repository.get(google_id)
        if user.admin:
            return True
        return False

    def correct_domain(self, user: User) -> bool:
        email_info = user.email.split("@")
        domain = email_info[1]
        if domain != "ioet.com":
            return False
        return True

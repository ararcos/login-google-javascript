from typing import Optional
from ..domain.services.user_service import UserService
from ..domain import User


class UserEditor:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, google_id: str, user: User) -> Optional[User]:
        return self.user_service.edit_user(google_id, user)

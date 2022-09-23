from typing import Optional

from ..domain.services.user_service import UserService
from ..domain import User


class UserGetter:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, google_id: str) -> Optional[User]:
        return self.user_service.get_user(google_id)

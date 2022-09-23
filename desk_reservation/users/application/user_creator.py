from ..domain.entities.user import User
from ..domain.services.user_service import UserService


class UserCreator:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, google_id: str, user: User) -> User:
        return self.user_service.create_user(google_id, user)

from ..domain.services.user_service import UserService


class UserDeleter:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, google_id: str, user_id: str) -> bool:
        return self.user_service.delete_user(google_id, user_id)

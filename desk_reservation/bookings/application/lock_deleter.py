from ..domain.services import LockService


class LockDeleter:
    def __init__(self, lock_service: LockService):
        self.lock_service = lock_service

    def execute(self, booking_id: str, user_id: str) -> bool:
        return self.lock_service.delete(
                booking_id=booking_id,
                user_id=user_id
            )

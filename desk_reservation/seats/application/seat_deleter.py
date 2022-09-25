from typing import Optional
from ..domain.entities.seat import Seat
from ..domain.services.seat_service import SeatService


class SeatDeleter:
    def __init__(self, seat_service: SeatService):
        self.seat_service = seat_service

    def execute(self, user_id: str, seat_id: str, office_id: str) -> Optional[Seat]:
        return self.seat_service.delete_seat(user_id=user_id, seat_id=seat_id, office_id=office_id)

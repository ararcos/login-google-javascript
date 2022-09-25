from typing import Optional

from ..domain.services.seat_service import SeatService
from ..domain import Seat


class SeatUpdater:
    def __init__(self, seat_service: SeatService):
        self.seat_service = seat_service

    def execute(self, user_id: str, seat: Seat) -> Optional[Seat]:
        return self.seat_service.update_seat(seat=seat, user_id=user_id)

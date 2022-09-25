from typing import Optional
from ..domain.entities.seat import Seat

from ..domain.services.seat_service import SeatService


class SeatGetter:
    def __init__(self, seat_service: SeatService):
        self.seat_service = seat_service

    def execute(self,  seat_id: str) -> Optional[Seat]:
        return self.seat_service.get_seat_by_id(seat_id)

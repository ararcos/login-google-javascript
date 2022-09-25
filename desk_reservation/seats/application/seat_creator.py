from ..domain.services.seat_service import SeatService
from ..domain.entities.seat import Seat


class SeatCreator:
    def __init__(self, seat_service: SeatService):
        self.seat_service = seat_service

    def execute(self, user_id: str, seat: Seat) -> Seat:
        return self.seat_service.create_seat(user_id=user_id, seat=seat)

from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ..domain.services.desk_service import DeskService


class DeskDeleter:
    def __init__(self, desk_service: DeskService):
        self.desk_service = desk_service

    def execute(self, user_id: str, desk_id: str) -> bool:
        desk = self.desk_service.get(desk_id)
        if not desk:
            raise IdNotFoundError("Desk", desk_id)
        self.desk_service.seat_repository.delete_many(desk.seats_list)
        return self.desk_service.delete(user_id, desk)

from ..domain import OfficeService


class OfficeDeleter:
    def __init__(self, office_service: OfficeService):
        self.office_service = office_service

    def execute(self, office_id: str, user_id: str) -> bool:
        return self.office_service.delete(office_id=office_id, user_id=user_id)

from typing import Optional

from ..domain import Office, OfficeService


class OfficeCreator:
    def __init__(self, office_service: OfficeService):
        self.office_service = office_service

    def execute(self, office: Office, user_id: str) -> Optional[Office]:
        return self.office_service.create(office=office, user_id=user_id)

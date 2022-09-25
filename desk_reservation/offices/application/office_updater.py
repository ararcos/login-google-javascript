from typing import Optional


from ..domain import Office, OfficeService


class OfficeUpdater:
    def __init__(self, office_service: OfficeService):
        self.office_service = office_service

    def execute(self, office_id: str, office: Office, user_id: str) -> Optional[Office]:
        return self.office_service.update(
            office=office,
            office_id=office_id,
            user_id=user_id
        )

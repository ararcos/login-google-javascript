from typing import Optional

from ..domain import Office, OfficeService


class OfficeFinderOne:
    def __init__(self, office_service: OfficeService):
        self.office_service = office_service

    def execute(self, office_id: str) -> Optional[Office]:
        return self.office_service.get(office_id=office_id)

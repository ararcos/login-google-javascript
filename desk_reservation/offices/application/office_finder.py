from typing import List

from ..domain import Office, OfficeService
from ...shared.infrastructure import Criteria


class OfficeFinder:
    def __init__(self, office_service: OfficeService):
        self.office_service = office_service

    def execute(self, criteria: Criteria) -> List[Office]:
        return self.office_service.find(criteria)

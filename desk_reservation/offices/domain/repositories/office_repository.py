from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.office import Office
from ....shared.infrastructure import Criteria


class OfficeRepository(ABC):
    @abstractmethod
    def get(self, office_id: str) -> Optional[Office]:
        pass

    @abstractmethod
    def create(self, office: Office) -> Office:
        pass

    @abstractmethod
    def update(self, office_id: str, office: Office) -> Optional[Office]:
        pass

    @abstractmethod
    def delete(self, office_id: str) -> bool:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[Office]:
        pass

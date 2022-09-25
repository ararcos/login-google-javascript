from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.desk import Desk
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria


class DeskRepository(ABC):
    @abstractmethod
    def create(self, desk: Desk) -> Desk:
        pass

    @abstractmethod
    def create_many(self, desk_list: List[Desk]) -> List[Desk]:
        pass

    @abstractmethod
    def get(self, desk_id: str) -> Optional[Desk]:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[Desk]:
        pass

    @abstractmethod
    def update(self, user_id: str, desk: Desk) -> Desk:
        pass

    @abstractmethod
    def delete(self, user_id:str, desk_id: str) -> bool:
        pass

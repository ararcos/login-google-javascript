from typing import List, Optional
from abc import ABC, abstractmethod

from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ..entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, google_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find(self, criteria: Criteria) -> List[User]:
        pass

    @abstractmethod
    def edit(self, google_id: str, user: User) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, google_id: str) -> bool:
        pass

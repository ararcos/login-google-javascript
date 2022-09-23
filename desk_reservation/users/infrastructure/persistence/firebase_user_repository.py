from typing import List, Optional

from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ...domain import UserRepository
from ...domain.entities.user import User


class FirebaseUserRepository(UserRepository):

    def __init__(self, firebase_repository: FirebaseRepository = None):
        self.user_reference = firebase_repository.data_base.collection("user")

    def create(self, user: User) -> User:
        doc_ref = self.user_reference.document(user.google_id)
        doc_ref.set(user.__dict__)
        return user

    def get(self, google_id: str) -> Optional[User]:
        doc_ref = self.user_reference.document(google_id)
        user= doc_ref.get()
        if user.exists:
            return User(**user.to_dict())
        return None

    def find(self, criteria: Criteria) -> List[User]:
        query = self.user_reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value)
        result = [User(**_doc.to_dict()) for _doc in query.get()]
        return result

    def edit(self, google_id:str, user: User) -> Optional[User]:
        doc_ref = self.user_reference.document(google_id)
        user_doc = doc_ref.get()
        if user_doc.exists:
            doc_ref.set(user.__dict__)
            return user
        return None

    def delete(self, google_id: str) -> bool:
        doc_ref = self.user_reference.document(google_id)
        user_doc = doc_ref.get()
        if user_doc.exists:
            doc_ref.update({'deleted': True})
            return True
        return False

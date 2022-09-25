from datetime import datetime
from typing import Dict, List, Optional


from ...domain import Desk, DeskRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository


class FirebaseDeskRepository(DeskRepository):
    def __init__(self, firebase_repository: FirebaseRepository = None):
        self.desk_reference = firebase_repository.data_base.collection("desk")

    def create(self, desk: Desk) -> Desk:
        desk_to_create = desk.__dict__
        desk_id = desk_to_create.pop("desk_id", None)
        doc_ref = self.desk_reference.document(desk_id)
        doc_ref.set(desk_to_create)
        return desk

    def create_many(self, desk_list: List[Desk]) -> List[Desk]:
        list_desk_created = map(self.create, desk_list)
        return list(list_desk_created)

    def get(self, desk_id: str) -> Optional[Desk]:
        doc_ref = self.desk_reference.document(desk_id)
        desk = doc_ref.get()
        if desk.exists:
            return Desk(**desk.to_dict()|{'desk_id': desk_id})
        return None

    def find(self, criteria: Criteria) -> List[Desk]:
        query = self.desk_reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value
                )
        result = [Desk(**_doc.to_dict()|{'desk_id': _doc.id}) for _doc in query.get()]
        return result

    def update(self, user_id: str, desk: Desk) -> Optional[Desk]:
        doc_ref = self.desk_reference.document(desk.desk_id)
        desk_doc = doc_ref.get()
        if desk_doc.exists:
            desk_to_update = desk.__dict__
            desk_to_update = {
                **desk_to_update,
                "updated_at:": datetime.now(),
                "updated_by": user_id,
            }
            doc_ref.set(desk_to_update)
            return desk
        return None

    def delete(self, user_id: str, desk_id: str) -> bool:
        doc_ref = self.desk_reference.document(desk_id)
        desk = doc_ref.get()
        if desk.exists:
            doc_ref.update({"deleted_at": datetime.now(), "deleted_by": user_id})
            return True
        return False

    def delete_many(self, desk_ids: List[str]) -> Dict:
        desk_created = map(self.delete, desk_ids)
        result = dict(zip(desk_ids, list(desk_created)))
        return result

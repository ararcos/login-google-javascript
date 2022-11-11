from datetime import datetime
from typing import List, Optional


from ...domain import Office, OfficeRepository
from ....shared.infrastructure import FirebaseRepository, Criteria


class FirebaseOfficeRepository(OfficeRepository):

    def __init__(self, firebase_repository: FirebaseRepository):
        self.office_reference = firebase_repository.data_base.collection('office')

    def create(self, office: Office) -> Office:
        doc_ref = self.office_reference.document(office.office_id)
        doc_ref.set(office.__dict__)
        return office


    def get(self, office_id: str) -> Optional[Office]:
        doc_ref = self.office_reference.document(office_id)
        office = doc_ref.get()
        if office.exists:
            return Office(**office.to_dict()|{'office_id': office.id})
        return None

    def find(self, criteria: Criteria) -> List[Office]:
        query = self.office_reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value)

        result = [Office(**_doc.to_dict()|{'office_id': _doc.id})
                  for _doc in query.get()]
        return result

    def update(self, office_id: str, office: Office) -> Optional[Office]:
        doc_ref = self.office_reference.document(office_id)
        doc = doc_ref.get()
        if doc.exists:
            office.__dict__.update(
                {'updated_at': datetime.now()})
            doc_ref.update(office.__dict__)
            return office
        return None

    def delete(self, office_id: str) -> bool:
        doc_ref = self.office_reference.document(office_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({'deleted_at': datetime.now()})
            return True
        return False

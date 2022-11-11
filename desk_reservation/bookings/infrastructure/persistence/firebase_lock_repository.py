from datetime import datetime
from typing import List

from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ...domain.entities import LockBooking
from ...domain.repositories import LockRepository

# pylint: disable=R0801
class FirebaseLockRepository(LockRepository):
    def __init__(self, firebase_repository: FirebaseRepository):
        self.lock_reference = firebase_repository.data_base.collection('locked_seat')

    def create(self, lock_booking: LockBooking) -> LockBooking:
        doc_ref = self.lock_reference.document(lock_booking.booking_id)
        doc_ref.set(lock_booking.__dict__)
        return lock_booking

    def find(self, criteria: Criteria) -> List[LockBooking]:
        query = self.lock_reference
        if criteria.filters:
            for _filter in criteria.filters:
                value = _filter.value
                if _filter.field in 'booked_date_init' or _filter.field == 'booked_date_end':
                    value = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                query = query.where(
                    _filter.field, _filter.operator.value, value
                )
        result = [LockBooking(**_doc.to_dict()|{'booking_id': _doc.id}) for _doc in query.get()]
        return result

    def delete(self, lock_id: str, user_id: str) -> bool:
        doc_ref = self.lock_reference.document(lock_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({'deleted_at': datetime.now()})
            doc_ref.update({'deleted_by': user_id})
            return True
        return False

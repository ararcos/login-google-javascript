from datetime import datetime
from typing import Optional, List

from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ...domain import Seat, SeatRepository


class FirebaseSeatRepository(SeatRepository):
    def __init__(self, firebase_repository: FirebaseRepository):
        self.reference = firebase_repository.data_base.collection("seats")

    def get(self, seat_id: str) -> Optional[Seat]:
        seat_ref = self.reference.document(seat_id)
        seat_data = seat_ref.get()
        if seat_data.exists:
            return Seat(**seat_data.to_dict())
        return None

    def find(self, criteria: Criteria) -> List[Seat]:
        query = self.reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value
                )
        result = [Seat(**_doc.to_dict()) for _doc in query.get()]
        return result

    def update(self, seat: Seat) -> Optional[Seat]:
        seat_ref = self.reference.document(seat.seat_id)
        seat_data = seat_ref.get()
        if seat_data.exists:
            seat_ref.set(seat.__dict__)
            return seat
        return None

    def create(self, seat: Seat) -> Seat:
        seat_ref = self.reference.document(seat.seat_id)
        seat_ref.set(seat.__dict__)
        return seat

    def create_many(self, seats: List[Seat]) -> List[Seat]:
        for seat in seats:
            self.create(seat)
        return seats

    def delete(self, seat_id: str) -> bool:
        seat_ref = self.reference.document(seat_id)
        seat_data = seat_ref.get()
        if seat_data.exists:
            seat_ref.update({"deleted_at": datetime.today()})
            return True
        return False

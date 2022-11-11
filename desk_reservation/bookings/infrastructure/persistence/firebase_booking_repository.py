from datetime import datetime
from typing import Optional, List

from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ...domain.entities import SeatBooking
from ...domain.repositories import BookingRepository

# pylint: disable=R0801
class FirebaseBookingRepository(BookingRepository):
    def __init__(self, firebase_repository: FirebaseRepository):
        self.booking_reference = firebase_repository.data_base.collection('booking_seats')

    def create(self, booking: SeatBooking) -> SeatBooking:
        doc_ref = self.booking_reference.document(booking.booking_id)
        doc_ref.set(booking.__dict__)
        return booking

    def create_many(self, bookings: List[SeatBooking]) -> List[SeatBooking]:
        for booking in bookings:
            self.create(booking)
        return bookings

    def get(self, booking_id: str) -> Optional[SeatBooking]:
        doc_ref = self.booking_reference.document(booking_id)
        doc = doc_ref.get()
        if doc.exists:
            return SeatBooking(**doc_ref.get().to_dict())
        return None

    def find(self, criteria: Criteria) -> List[SeatBooking]:
        query = self.booking_reference
        if criteria.filters:
            for _filter in criteria.filters:
                value = _filter.value
                if _filter.field in 'booked_date_init' or _filter.field == 'booked_date_end':
                    value = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                query = query.where(
                    _filter.field, _filter.operator.value, value
                )
        result = [SeatBooking(**_doc.to_dict()|{'booking_id': _doc.id}) for _doc in query.get()]
        return result

    def delete(self, booking_id: str, user_id: str) -> bool:
        doc_ref = self.booking_reference.document(booking_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({'deleted_at': datetime.now()})
            doc_ref.update({'deleted_by': user_id})
            return True
        return False

    def update(
        self,
        booking_id: str,
        updated_by: str,
        booking: SeatBooking) -> Optional[SeatBooking]:
        doc_ref = self.booking_reference.document(booking_id)
        doc = doc_ref.get()
        if doc.exists:
            booking.updated_at = datetime.now()
            booking.updated_by = updated_by
            doc_ref.update(booking.__dict__)
            return booking
        return None

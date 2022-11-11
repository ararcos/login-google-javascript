from datetime import datetime
from typing import Optional, List

from desk_reservation.bookings.domain.repositories.booking_parking_repository import (
    BookingParkingRepository,
)

from ...domain.entities.booking import ParkingBooking
from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria

# pylint: disable=R0801
class FirebaseBookingParkingRepository(BookingParkingRepository):
    def __init__(self, firebase_repository: FirebaseRepository):
        self.booking_reference = firebase_repository.data_base.collection(
            "booking_parking"
        )

    def create(self, booking: ParkingBooking) -> ParkingBooking:
        doc_ref = self.booking_reference.document(booking.booking_id)
        doc_ref.set(booking.__dict__)
        return booking

    def find(self, criteria: Criteria) -> List[ParkingBooking]:
        query = self.booking_reference
        if criteria.filters:
            for _filter in criteria.filters:
                value = _filter.value
                if (
                    _filter.field in "booked_date_init"
                    or _filter.field == "booked_date_end"
                ):
                    value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                query = query.where(_filter.field, _filter.operator.value, value)
        result = [
            ParkingBooking(**_doc.to_dict() | {"booking_id": _doc.id})
            for _doc in query.get()
        ]
        return result

    def delete(self, booking_id: str, user_id: str) -> bool:
        doc_ref = self.booking_reference.document(booking_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({"deleted_at": datetime.now()})
            doc_ref.update({"deleted_by": user_id})
            return True
        return False

    def update(
        self, booking_id: str, updated_by: str, booking: ParkingBooking
    ) -> Optional[ParkingBooking]:
        doc_ref = self.booking_reference.document(booking_id)
        doc = doc_ref.get()
        if doc.exists:
            booking.updated_at = datetime.now()
            booking.updated_by = updated_by
            doc_ref.update(booking.__dict__)
            return booking
        return None

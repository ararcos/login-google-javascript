from datetime import datetime
from typing import List, Optional


from ....shared.domain import BadRequestError
from ....shared.infrastructure import FirebaseRepository, Criteria
from ...domain import RideRepository, Ride, RideBooking


class FirebaseRideRepository(RideRepository):

    def __init__(self, firebase_repository: FirebaseRepository = None):
        self.ride_reference = firebase_repository.data_base.collection('ride')
        self.ride_booking_reference = firebase_repository.data_base.collection(
            'booking_ride')

    def create(self, ride: Ride) -> Ride:
        ride_to_create = ride.__dict__
        ride_id = ride_to_create.pop('ride_id', None)
        if ride_id:
            doc_ref = self.ride_reference.document(ride_id)
            doc = doc_ref.set(ride_to_create)
            ride.ride_id = doc.id
            return ride
        raise BadRequestError('field ride_id is required')

    def find_by_id(self, ride_id: str) -> Optional[Ride]:
        doc_ref = self.ride_reference.document(ride_id)
        ride = doc_ref.get()
        if ride.exists:
            return Ride(**ride.to_dict()|{'ride_id': ride_id})
        return None

    def find_all(self, criteria: Criteria) -> List[Ride]:
        query = self.ride_reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value)

        result = [Ride(**_doc.to_dict()|{'ride_id': _doc.id})
                  for _doc in query.get()]
        return result

    def update(self, user_id: str, ride_id: str, ride: Ride) -> Optional[Ride]:
        doc_ref = self.ride_reference.document(ride_id)
        doc = doc_ref.get()
        if doc.exists:
            ride_to_update = ride.__dict__.update(
                {'updated_at': datetime.now(), 'updated_by': user_id})
            doc_ref.update(ride_to_update)
            return ride
        return None

    def delete(self, ride_id: str) -> bool:
        doc_ref = self.ride_reference.document(ride_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({'deleted_at': datetime.now()})
            return True
        return False

    def booking_ride(self, ride_booking: RideBooking) -> Optional[RideBooking]:
        ride_ref = self.ride_reference.document(ride_booking.ride_id)
        ride = self.find_by_id(ride_booking.ride_id)
        if ride:
            booking_ride_to_create = ride_booking.__dict__
            ride_booking_id = booking_ride_to_create.pop('ride_booking_id', None)
            if ride_booking_id:
                doc_ref = self.ride_booking_reference.document(ride_booking_id)
                doc = doc_ref.set(booking_ride_to_create)
                ride_booking.ride_booking_id = doc.id
                ride.passengers.append(doc.id)
                ride_ref.update({'passengers': ride.passengers})
                return ride_booking
            raise BadRequestError('field ride_booking_id is required')
        return None

    def find_booking_ride(self, criteria: Criteria) -> List[RideBooking]:
        query = self.ride_booking_reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value)

        result = [RideBooking(**_doc.to_dict()|{'ride_booking_id': _doc.id})
                  for _doc in query.get()]
        return result

    def find_by_id_booking_ride(self, ride_booking_id: str) -> Optional[RideBooking]:
        doc_ref = self.ride_booking_reference.document(ride_booking_id)
        ride_booking = doc_ref.get()
        if ride_booking.exists:
            return RideBooking(**ride_booking.to_dict()|{'ride_booking_id': ride_booking_id})
        return None

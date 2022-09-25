import typing
from datetime import datetime, time

from ..entities import SeatBooking
from ..exceptions import InvalidDateRange, UserAlreadyHasReservation
from ..repositories import BookingRepository
from ....users.domain import UserRepository
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.infrastructure.firestore.firestore_criteria import (
    Criteria, Filter, Operator
)


class BookingService:
    def __init__(self, user_repository: UserRepository, booking_repository: BookingRepository):
        self.user_repository = user_repository
        self.booking_repository = booking_repository

    def create_booking(self, booking: SeatBooking) -> SeatBooking:
        self.dates_booking_validator(booking=booking)
        user_bookings = self.user_reservations_by_dates(
            date_init=booking.booked_date_init,
            date_end=booking.booked_date_end,
            user_id=booking.booked_by['google_id']
        )
        if user_bookings:
            raise UserAlreadyHasReservation(
                'The user already has a reservation',
                [_booking.booking_id for _booking in user_bookings]
            )

        return self.booking_repository.create(booking)

    def create_bookings(self, bookings: typing.List[SeatBooking]) -> typing.List[SeatBooking]:
        validated_booking_dates = [
            _booking.booked_date_init
            for _booking in bookings
            if self.dates_booking_validator(_booking)
        ]
        user_bookings = self.user_reservations_by_dates(
            date_init=min(validated_booking_dates),
            date_end=max(validated_booking_dates),
            user_id=bookings[0].booked_by['google_id']
        )
        if user_bookings:
            raise UserAlreadyHasReservation(
                'The user already has a reservation',
                [_booking.booking_id for _booking in user_bookings]
            )

        return self.booking_repository.create_many(bookings)

    def get_booking_by_id(self, booking_id: str) -> typing.Optional[SeatBooking]:
        result = self.booking_repository.get(booking_id)
        if result:
            return result
        raise IdNotFoundError('seatBooking', booking_id)

    def find_bookings(self, criteria: Criteria) -> typing.List[SeatBooking]:
        return self.booking_repository.find(criteria)

    def update_booking(self, booking_id: str, user_id: str, booking: SeatBooking) -> SeatBooking:
        result = self.booking_repository.update(
            booking_id=booking_id, updated_by=user_id , booking=booking
        )
        if result:
            return result
        raise IdNotFoundError('seatBooking', booking_id)


    def delete_booking(self, booking_id: str, user_id: str) -> bool:
        result = self.booking_repository.delete(booking_id, user_id)
        if not result:
            raise IdNotFoundError("Booking", booking_id)
        return result

    def booking_can_be_edited(self, booking: SeatBooking, user_id: str) -> bool:
        user = self.user_repository.get(google_id=user_id)
        if booking.booked_date_end < datetime.today():
            return False
        if hasattr(user, 'admin') and user.admin or booking.booked_by['google_id'] == user_id:
            return True
        return False

    def user_reservations_by_dates(
            self, date_init: datetime, date_end: datetime, user_id: str
    ) -> typing.List[SeatBooking]:
        start_of_day = datetime.combine(date_init, time.min)
        end_of_day = datetime.combine(date_end, time.max)
        criteria_to_find_reservations = Criteria(
            filters=[
                Filter(
                    field='booked_by.google_id', operator=Operator.EQUAL, value=user_id
                ),
                Filter(
                    field='booked_date_init',
                    operator=Operator.GREATER_EQUAL_THAN,
                    value=start_of_day
                ),
                Filter(
                    field='booked_date_init',
                    operator=Operator.LOWER_EQUAL_THAN,
                    value=end_of_day
                )
            ]
        )
        return self.find_bookings(criteria=criteria_to_find_reservations)

    def dates_booking_validator(self, booking: SeatBooking) -> bool:
        if booking.booked_date_init.date() != booking.booked_date_end.date():
            raise InvalidDateRange(
                'The booking cannot be on different days,'
                ' For an extended booking create multiples records'
            )
        if booking.booked_date_init < datetime.combine(datetime.today(), time.min):
            raise InvalidDateRange(
                'It is not possible to create a reserve in the past'
            )
        return True

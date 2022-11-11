import typing
from datetime import datetime, time
from desk_reservation.bookings.domain.entities.booking import ParkingBooking
from desk_reservation.bookings.domain.exceptions.invalid_date_range_error import (
    InvalidDateRange,
)
from desk_reservation.bookings.domain.exceptions.user_already_has_a_reservation import (
    UserAlreadyHasReservation,
)
from desk_reservation.bookings.domain.repositories.booking_parking_repository import (
    BookingParkingRepository,
)
from desk_reservation.offices.domain.repositories.office_repository import (
    OfficeRepository,
)
from desk_reservation.parkings.domain.repositories.parking_repository import ParkingRepository
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError

from desk_reservation.users.domain.repositories.user_repository import UserRepository
from ....shared.infrastructure.firestore.firestore_criteria import (
    Criteria,
    Filter,
    Operator,
)


class BookingParkingService:
    def __init__(
        self,
        user_repository: UserRepository,
        booking_parking_repository: BookingParkingRepository,
        parking_repository: ParkingRepository,
        office_repository: OfficeRepository,
    ):
        self.user_repository = user_repository
        self.booking_parking_repository = booking_parking_repository
        self.parking_repository = parking_repository
        self.office_repository = office_repository

    def create_parking_booking(self, booking: ParkingBooking) -> ParkingBooking:
        self.dates_parking_booking_validator(booking=booking)
        user_parking_bookings = self.user_reservations_by_dates(
            date_init=booking.booked_date_init,
            date_end=booking.booked_date_end,
            user_id=booking.booked_by["google_id"],
        )
        if user_parking_bookings:
            office_of_conflict = self.office_repository.get(user_parking_bookings[0].office_id)
            raise UserAlreadyHasReservation(
                f"You already booked a desk this date ({booking.booked_date_init.date()})"
                f" at {office_of_conflict.name.capitalize()} parking",
                [_booking.booking_id for _booking in user_parking_bookings],
            )

        return self.booking_parking_repository.create(booking)

    def find_parking_bookings(self, criteria: Criteria) -> typing.List[ParkingBooking]:
        bookings = self.booking_parking_repository.find(criteria)
        return bookings

    def update_parking_booking(
        self, booking_id: str, user_id: str, booking: ParkingBooking
    ) -> ParkingBooking:
        result = self.booking_parking_repository.update(
            booking_id=booking_id, updated_by=user_id, booking=booking
        )
        if result:
            return result
        raise IdNotFoundError("ParkingBooking", booking_id)

    def delete_parking_booking(self, booking_id: str, user_id: str) -> bool:
        result = self.booking_parking_repository.delete(booking_id, user_id)
        if not result:
            raise IdNotFoundError("Booking", booking_id)
        return result

    def parking_booking_can_be_edited(self, booking: ParkingBooking, user_id: str) -> bool:
        user = self.user_repository.get(google_id=user_id)
        if booking.booked_date_end < datetime.today():
            return False
        if (
            hasattr(user, "admin")
            and user.admin
            or booking.booked_by["google_id"] == user_id
        ):
            return True
        return False

    def user_reservations_by_dates(
        self, date_init: datetime, date_end: datetime, user_id: str
    ) -> typing.List[ParkingBooking]:
        start_of_day = datetime.combine(date_init, time.min)
        end_of_day = datetime.combine(date_end, time.max)
        criteria_to_find_reservations = Criteria(
            filters=[
                Filter(
                    field="booked_by.google_id", operator=Operator.EQUAL, value=user_id
                ),
                Filter(
                    field="booked_date_init",
                    operator=Operator.GREATER_EQUAL_THAN,
                    value=start_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                Filter(
                    field="booked_date_init",
                    operator=Operator.LOWER_EQUAL_THAN,
                    value=end_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                Filter(field="deleted_at", operator=Operator.EQUAL, value=None),
            ]
        )
        return self.find_parking_bookings(criteria=criteria_to_find_reservations)

    def dates_parking_booking_validator(self, booking: ParkingBooking) -> bool:
        if booking.booked_date_init.date() != booking.booked_date_end.date():
            raise InvalidDateRange(
                "The booking cannot be on different days,"
                " For an extended booking create multiples records"
            )
        if booking.booked_date_init < datetime.combine(datetime.today(), time.min):
            raise InvalidDateRange("It is not possible to create a reserve in the past")
        return True

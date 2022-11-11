from faker import Faker

from desk_reservation.bookings.application.booking_getter import BookingGetter


def test___booking_getter__was_called_correctly(mocker):
    booking_service = mocker.Mock()
    booking_getter = BookingGetter(booking_service=booking_service)
    booking_id = Faker().uuid4()

    booking_getter.execute(booking_id=booking_id)

    booking_getter.booking_service.get_booking_by_id.assert_called_with(booking_id=booking_id)

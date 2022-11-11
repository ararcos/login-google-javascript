from faker import Faker

from desk_reservation.bookings.application import BookingUpdater

def test__booking_updater__was_called_correctly(mocker, seat_booking_factory):
    booking_id=Faker().uuid4()
    user_id=Faker().uuid4()
    booking_service = mocker.Mock()
    booking_updater = BookingUpdater(booking_service=booking_service)
    booking = seat_booking_factory()

    booking_updater.execute(
        booking_id=booking_id,
        user_id=user_id,
        booking=booking
        )

    booking_updater.booking_service.update_booking.assert_called_with(
        booking_id=booking_id,
        user_id=user_id,
        booking=booking
        )

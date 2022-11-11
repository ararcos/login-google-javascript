from faker import Faker

from desk_reservation.bookings.application.booking_parking_updater import BookingParkingUpdater



def test__booking_parking_updater__was_called_correctly(mocker, parking_booking_factory):
    booking_id=Faker().uuid4()
    user_id=Faker().uuid4()
    booking_parking_service = mocker.Mock()
    booking_parking_updater = BookingParkingUpdater(booking_parking_service=booking_parking_service)
    booking = parking_booking_factory()

    booking_parking_updater.execute(
        booking_id=booking_id,
        user_id=user_id,
        booking=booking
        )

    booking_parking_updater.booking_parking_service.update_parking_booking.assert_called_with(
        booking_id=booking_id,
        user_id=user_id,
        booking=booking
        )

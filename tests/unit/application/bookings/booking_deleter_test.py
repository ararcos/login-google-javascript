from faker import Faker
from desk_reservation.bookings.application.booking_deleter import BookingDeleter

def test__booking_deleter__was_called_correctly(mocker):
    user_id=Faker().uuid4()
    booking_id=Faker().uuid4()
    booking_service = mocker.Mock()
    booking_deleter = BookingDeleter(booking_service=booking_service)

    booking_deleter.execute(booking_id=booking_id, user_id=user_id)

    booking_deleter.booking_service.delete_booking.assert_called_with(booking_id=booking_id, user_id=user_id)

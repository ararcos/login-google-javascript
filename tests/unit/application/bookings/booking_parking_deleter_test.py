from faker import Faker

from desk_reservation.bookings.application.booking_parking_deleter import BookingParkingDeleter

def test__booking_parking_deleter__was_called_correctly(mocker):
    user_id=Faker().uuid4()
    booking_id=Faker().uuid4()
    booking_parking_service = mocker.Mock()
    booking_deleter = BookingParkingDeleter(booking_parking_service=booking_parking_service)

    booking_deleter.execute(booking_id=booking_id, user_id=user_id)

    booking_deleter.booking_parking_service.delete_parking_booking.assert_called_with(booking_id=booking_id, user_id=user_id)
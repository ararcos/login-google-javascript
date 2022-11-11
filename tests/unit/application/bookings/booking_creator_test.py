from desk_reservation.bookings.application import BookingCreator

def test__booking_creator__was_called_correctly(mocker, seat_booking_factory):
    booking_service = mocker.Mock()
    booking_creator = BookingCreator(booking_service=booking_service)
    booking = seat_booking_factory()

    booking_creator.execute(booking)

    booking_creator.booking_service.create_booking.assert_called_with(booking)

from desk_reservation.bookings.application.booking_parking_creator import BookingParkingCreator

def test__booking_parking_creator__was_called_correctly(mocker, parking_booking_factory):
    booking_parking_service = mocker.Mock()
    booking_creator = BookingParkingCreator(booking_parking_service=booking_parking_service)
    parking_booking = parking_booking_factory()

    booking_creator.execute(parking_booking)

    booking_creator.booking_parking_service.create_parking_booking.assert_called_with(parking_booking)




from desk_reservation.bookings.application.booking_parking_finder import BookingParkingFinder


def test__find_parking_bookings_was_called_correctly(mocker):
    criteria = mocker.Mock()
    booking_parking_service = mocker.Mock(find=mocker.Mock())
    booking_finder = BookingParkingFinder(booking_parking_service=booking_parking_service)

    booking_finder.execute(criteria)

    booking_parking_service.find_parking_bookings.assert_called_with(criteria)

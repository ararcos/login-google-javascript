from desk_reservation.bookings.application import BookingFinder


def test__find_bookings_was_called_correctly(mocker):
    criteria = mocker.Mock()
    booking_service = mocker.Mock(find=mocker.Mock())
    booking_finder = BookingFinder(booking_service=booking_service)

    booking_finder.execute(criteria,True)

    booking_service.find_bookings.assert_called_with(criteria, True)

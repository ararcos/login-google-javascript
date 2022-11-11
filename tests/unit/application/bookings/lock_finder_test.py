from desk_reservation.bookings.application import LockFinder


def test__find_lock_bookings_was_called_correctly(mocker):
    criteria = mocker.Mock()
    lock_service = mocker.Mock(find=mocker.Mock())
    lock_finder = LockFinder(lock_service=lock_service)

    lock_finder.execute(criteria)

    lock_service.find.assert_called_with(criteria)

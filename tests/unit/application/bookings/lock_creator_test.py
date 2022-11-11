from desk_reservation.bookings.application import LockCreator

def test__lock_creator__was_called_correctly(mocker, lock_booking_factory):
    lock_service = mocker.Mock()
    lock_creator = LockCreator(lock_service=lock_service)
    lock_booking = lock_booking_factory()

    lock_creator.execute(lock_booking)

    lock_creator.lock_service.create.assert_called_with(lock_booking)

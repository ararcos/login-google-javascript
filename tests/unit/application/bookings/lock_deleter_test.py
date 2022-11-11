from faker import Faker
from desk_reservation.bookings.application import LockDeleter

def test__lock_deleter__was_called_correctly(mocker):
    user_id=Faker().uuid4()
    booking_id=Faker().uuid4()
    lock_service = mocker.Mock()
    lock_deleter = LockDeleter(lock_service=lock_service)

    lock_deleter.execute(booking_id=booking_id, user_id=user_id)

    lock_deleter.lock_service.delete.assert_called_with(booking_id=booking_id, user_id=user_id)

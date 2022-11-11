from faker import Faker
import pytest

from desk_reservation.bookings.domain.services.lock_service import LockService
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    lock_repository = mocker.Mock()
    lock_service = LockService(
        lock_repository=lock_repository,
    )
    return {
        'lock_repository': lock_repository,
        'service': lock_service,
    }

def test__create__was_called_correctly(dependencies, lock_booking_factory):
    lock_repository, service = dependencies.values()
    lock_booking = lock_booking_factory()

    service.create(lock_booking)

    lock_repository.create.assert_called_with(lock_booking)

def test__find_lock_bookings__was_called_correctly(dependencies, mocker):
    lock_repository, service = dependencies.values()
    criteria = mocker.Mock()

    service.find(criteria)

    lock_repository.find.assert_called_with(criteria)

def test__delete_lock_booking__was_called_correctly(dependencies, mocker):
    lock_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    lock_repository.delete = mocker.Mock(return_value=True)

    result = service.delete(booking_id, user_id)

    assert result is True

def test__delete_lock_booking__was_called_when_id_is_not_found(dependencies, mocker):
    lock_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    lock_repository.delete = mocker.Mock(return_value=False)

    with pytest.raises(IdNotFoundError):
        service.delete(booking_id, user_id)

import json
import pytest
from faker import Faker
from typing import Callable
from http import HTTPStatus
from desk_reservation.bookings.application import LockFinder
from desk_reservation.bookings.infrastructure.controllers.find_lock import find_lock_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name='mocked_lock_finder')
def _mocked_library(mocker) -> Callable:
    def _create_booking_finder(lock_finder: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.find_lock.lock_booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(LockFinder, 'execute',
                            side_effect=lock_finder)
    return _create_booking_finder


def test__find_lock_controller__return_bookings(
    mocked_lock_finder,
    mocker,
    lock_booking_factory
):
    seat_id = Faker().uuid4()
    lock_booking = lock_booking_factory(
        seat_id=seat_id
    )
    mocked_lock_finder(mocker.Mock(return_value=[lock_booking]))
    event = {'queryStringParameters': {'filters': json.dumps([
        {'field': "seat_id", "value": seat_id, "operator": "EQUAL"}])}}

    result = find_lock_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([lock_booking.__dict__], default=str)


def test__find_lock_controller__dont_return_seats(
    mocked_lock_finder,
    mocker,
):
    mocked_lock_finder(mocker.Mock(return_value=[]))
    event = {'filters': {'items': mocker.Mock()}for _ in range(3)}

    result = find_lock_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([])


def test__find_lock_controller__raises_domain_error(
    mocked_lock_finder,
    mocker,
):
    mocked_lock_finder(DomainError("Internal server error"))
    event = {'filters': {'items': mocker.Mock()}for _ in range(3)}

    result = find_lock_controller(event)
    assert result['status_code'] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result['body'] == json.dumps({'message': "Internal server error"})

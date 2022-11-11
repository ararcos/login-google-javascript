from email.policy import default
import json
import pytest
from faker import Faker
from typing import Callable
from http import HTTPStatus
from desk_reservation.bookings.application.booking_finder import BookingFinder
from desk_reservation.bookings.infrastructure.controllers.find_booking import find_booking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name='mocked_booking_finder')
def _mocked_library(mocker) -> Callable:
    def _create_booking_finder(booking_finder: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.find_booking.booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(BookingFinder, 'execute',
                            side_effect=booking_finder)
    return _create_booking_finder


def test__find_booking_controller__return_bookings(
    mocked_booking_finder,
    mocker,
    seat_factory
):
    seat_id = Faker().uuid4()
    booking = seat_factory(
        seat_id=seat_id
    )
    mocked_booking_finder(mocker.Mock(return_value=[booking]))
    event = {'queryStringParameters': {'filters': [
        {'field': "seat_id", "value": seat_id, "operator": "EQUAL"}]}}

    result = find_booking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([booking.__dict__], default=str)


def test__find_booking_controller__dont_return_seats(
    mocked_booking_finder,
    mocker,
):
    mocked_booking_finder(mocker.Mock(return_value=[]))

    event = {'queryStringParameters': {'filters': [
        {'field': "seat_id", "value": 2, "operator": "EQUAL"}]}}


    result = find_booking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([])


def test__find_booking_controller__raises_domain_error(
    mocked_booking_finder,
    mocker,
):
    mocked_booking_finder(DomainError("Internal server error"))

    event = {'queryStringParameters': {'filters': [
        {'field': "seat_id", "value": 2, "operator": "EQUAL"}]}}

    result = find_booking_controller(event)
    assert result['status_code'] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result['body'] == json.dumps({'message': "Internal server error"})

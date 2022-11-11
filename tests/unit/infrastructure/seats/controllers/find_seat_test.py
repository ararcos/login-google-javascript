import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.seats.application.seat_finder import SeatFinder
from desk_reservation.seats.infrastructure.controllers.find_seat import find_seat_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_seat_finder')
def _mocked_library(mocker) -> Callable:
    def _create_seat_finder(seat_finder: any) -> None:
        mocker.patch('desk_reservation.seats.infrastructure.controllers.find_seat.seat_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(SeatFinder, 'execute',
                            side_effect=seat_finder)
    return _create_seat_finder


def test__find_seat_controller__return_seats(mocked_seat_finder, mocker, seat_factory):
    seats = [seat_factory() for _ in range(3)]
    mocked_seat_finder(mocker.Mock(return_value=seats))
    event = {}
    result = find_seat_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([seat.__dict__ for seat in seats], default=str)
    
def test__find_seat_controller__dont_return_seats(mocked_seat_finder, mocker, seat_factory):
    mocked_seat_finder(mocker.Mock(return_value=[]))

    event = {}
    result = find_seat_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([])
    

def test__find_seat_controller__raise_DomainError(mocked_seat_finder, mocker, seat_factory):
    mocked_seat_finder(DomainError("An external error ocurred"))

    event = {}
    result = find_seat_controller(event)
    assert result['status_code'] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    

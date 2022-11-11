import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.seats.application import SeatGetter
from desk_reservation.seats.infrastructure.controllers.get_seat import get_seat_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError



@pytest.fixture(name='mocked_seat_getter')
def _mocked_library(mocker) -> Callable:
    def _create_seat_getter(seat_getter: any) -> None:
        mocker.patch('desk_reservation.seats.infrastructure.controllers.get_seat.seat_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(SeatGetter, 'execute',
                            side_effect=seat_getter)
    return _create_seat_getter


def test__return_seat_when_seat_id_exist(mocked_seat_getter, mocker, seat_factory):
    seat = seat_factory()
    mocked_seat_getter(mocker.Mock(return_value=seat))

    result = get_seat_controller({'seat_id': seat.seat_id})
    assert result['status_code'] == HTTPStatus.FOUND
    assert result['body'] == json.dumps(seat.__dict__, default=str)
    
    
def test__return_raise_idnotfound_when_seat_id_doesnt_exist(mocked_seat_getter, mocker, seat_factory):
    seat = seat_factory()
    mocked_seat_getter(IdNotFoundError("Seat",seat.seat_id))

    result = get_seat_controller({'seat_id': seat.seat_id})
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Seat id:'"+ seat.seat_id +"' not found"})


def test__return_raise_DomainError(mocked_seat_getter, mocker, seat_factory):
    seat = seat_factory()
    mocked_seat_getter(DomainError("An external error ocurred"))

    result = get_seat_controller({'seat_id': seat.seat_id})
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    
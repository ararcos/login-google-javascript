import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.seats.application.seat_deleter import SeatDeleter
from desk_reservation.seats.infrastructure.controllers.delete_seat import delete_seat_controller
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_seat_deleter')
def _mocked_library(mocker) -> Callable:
    def _create_seat_deleter(seat_deleter: any) -> None:
        mocker.patch('desk_reservation.seats.infrastructure.controllers.delete_seat.seat_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(SeatDeleter, 'execute',
                            side_effect=seat_deleter)
    return _create_seat_deleter


def test__delete_seat_controller__return_seat(mocked_seat_deleter, mocker, seat_factory):
    seat_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)
    mocked_seat_deleter(mocker.Mock(return_value=seat))
    event = {"body":json.dumps({'seat_id': seat_id, 'user_id': user_id, 'office_id': office_id}, default=str)}

    result = delete_seat_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(seat.__dict__, default=str)
    

def test__delete_seat_controller__raise_idNotFoundError(mocked_seat_deleter, mocker, seat_factory):
    seat_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)
    mocked_seat_deleter(IdNotFoundError("Seat",seat.seat_id))
    event = {"body":json.dumps({'seat_id': seat_id, 'user_id': user_id, 'office_id': office_id}, default=str)}

    result = delete_seat_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Seat id:'"+ seat.seat_id +"' not found"})
    

def test__delete_seat_controller__raise_PermissionsError(mocked_seat_deleter):
    seat_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    mocked_seat_deleter(PermissionsError("delete a seat"))
    event = {"body":json.dumps({'seat_id': seat_id, 'user_id': user_id, 'office_id': office_id}, default=str)}

    result = delete_seat_controller(event)
    assert result['status_code'] == HTTPStatus.UNAUTHORIZED
    assert result['body'] == json.dumps({'message': "You don't have permissions: <delete a seat>"})
    

def test__delete_seat_controller__raise_DomainError(mocked_seat_deleter):
    seat_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    mocked_seat_deleter(DomainError("An external error ocurred"))
    event = {"body":json.dumps({'seat_id': seat_id, 'user_id': user_id, 'office_id': office_id}, default=str)}

    result = delete_seat_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
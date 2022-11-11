import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.seats.application.seat_updater import SeatUpdater
from desk_reservation.seats.infrastructure.controllers.update_seat import update_seat_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_seat_updater')
def _mocked_library(mocker) -> Callable:
    def _create_seat_updater(seat_updater: any) -> None:
        mocker.patch('desk_reservation.seats.infrastructure.controllers.update_seat.seat_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(SeatUpdater, 'execute',
                            side_effect=seat_updater)
    return _create_seat_updater


def test__update_seat_controller__return_seat(mocked_seat_updater, mocker, seat_factory):
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory()
    mocked_seat_updater(mocker.Mock(return_value=seat))
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id, 'office_id': office_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(seat.__dict__, default=str)
    

def test__update_seat_controller__raise_idNotFoundError(mocked_seat_updater, mocker, seat_factory):
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory()
    mocked_seat_updater(IdNotFoundError("Seat",seat.seat_id))
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id, 'office_id': office_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Seat id:'"+ seat.seat_id +"' not found"})
    

def test__update_seat_controller__raise_PermissionsError(mocked_seat_updater, mocker, seat_factory):
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory()
    mocked_seat_updater(PermissionsError("update a seat"))
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id, 'office_id': office_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.UNAUTHORIZED
    assert result['body'] == json.dumps({'message': "You don't have permissions: <update a seat>"})
    
def test__update_seat_controller__raise_NameAlreadyExistsError(mocked_seat_updater, seat_factory, user_factory):
    user_id = Faker().uuid4()
    user = user_factory()
    seat = seat_factory()
    mocked_seat_updater(NameAlreadyExistsError("Seat", seat.name))
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps({'message': "Cannot create a new <Seat>, Name: "+ seat.name +" already exists"})
    
    
def test__update_seat_controller__raise_ValidationError(mocked_seat_updater, mocker, seat_factory):
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory()
    seat_dict = seat.__dict__
    del seat_dict['seat_id']
    mocked_seat_updater(mocker.Mock())
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id, 'office_id': office_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps({'message': "Check seat attributes"})
    
def test__update_seat_controller__raise_DomainError(mocked_seat_updater, mocker, seat_factory):
    office_id=Faker().uuid4()
    user_id=Faker().uuid4()
    seat = seat_factory()
    mocked_seat_updater(DomainError("An external error ocurred"))
    event = {"body":json.dumps({**seat.__dict__,'user_id': user_id, 'office_id': office_id}, default=str)}

    result = update_seat_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    
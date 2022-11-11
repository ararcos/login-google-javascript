import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.parkings.application.parking_updater import ParkingUpdater
from desk_reservation.parkings.infrastructure.controllers.update_parking import update_parking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_parking_updater')
def _mocked_library(mocker) -> Callable:
    def _create_parking_updater(parking_updater: any) -> None:
        mocker.patch('desk_reservation.parkings.infrastructure.controllers.update_parking.parking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(ParkingUpdater, 'execute',
                            side_effect=parking_updater)
    return _create_parking_updater


def test__update_parking_controller__return_parking(mocked_parking_updater, mocker, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    mocked_parking_updater(mocker.Mock(return_value=parking))
    event = {'user': user.__dict__, 'parking': parking.__dict__}

    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(parking.__dict__, default=str)
    

def test__update_parking_controller__raise_idNotFoundError(mocked_parking_updater, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    mocked_parking_updater(IdNotFoundError("Parking",parking.parking_id))
    event = {'user': user.__dict__, 'parking': parking.__dict__}
    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Parking id:'"+ parking.parking_id +"' not found"})
    

def test__update_parking_controller__raise_PermissionsError(mocked_parking_updater, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    mocked_parking_updater(PermissionsError("update a parking"))
    event = {'user': user.__dict__, 'parking': parking.__dict__}

    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.UNAUTHORIZED
    assert result['body'] == json.dumps({'message': "You don't have permissions: <update a parking>"})
    

def test__update_parking_controller__raise_NameAlreadyExistsError(mocked_parking_updater, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    mocked_parking_updater(NameAlreadyExistsError("Parking", parking.name))
    event = {'user': user.__dict__, 'parking': parking.__dict__}

    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps({'message': "Cannot create a new <Parking>, Name: "+ parking.name +" already exists"})
    

    
def test__update_parking_controller__raise_ValidationError(mocked_parking_updater, mocker, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    parking_dict = parking.__dict__
    del parking_dict['parking_id']
    mocked_parking_updater(mocker.Mock())
    event = {'user': user.__dict__, 'parking': parking_dict}

    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps({'message': "Check parking attributes"})
    
def test__update_parking_controller__raise_DomainError(mocked_parking_updater, parking_factory, user_factory):
    user = user_factory()
    parking = parking_factory()
    mocked_parking_updater(DomainError("An external error ocurred"))
    event = {'user': user.__dict__, 'parking': parking.__dict__}

    result = update_parking_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    
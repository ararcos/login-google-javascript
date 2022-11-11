import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.parkings.application.parking_deleter import ParkingDeleter
from desk_reservation.parkings.infrastructure.controllers.delete_parking import delete_parking_controller
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_parking_deleter')
def _mocked_library(mocker) -> Callable:
    def _create_parking_deleter(parking_deleter: any) -> None:
        mocker.patch('desk_reservation.parkings.infrastructure.controllers.delete_parking.parking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(ParkingDeleter, 'execute',
                            side_effect=parking_deleter)
    return _create_parking_deleter


def test__delete_parking_controller__return_parking(mocked_parking_deleter, mocker, parking_factory, user_factory):
    parking_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user = user_factory()
    parking = parking_factory(parking_id=parking_id)
    mocked_parking_deleter(mocker.Mock(return_value=parking))
    event = {'parking_id': parking_id, 'user': user.__dict__, 'office_id': office_id}

    result = delete_parking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(parking.__dict__, default=str)
    

def test__delete_parking_controller__raise_idNotFoundError(mocked_parking_deleter, parking_factory, user_factory):
    parking_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user = user_factory()
    parking = parking_factory(parking_id=parking_id)
    mocked_parking_deleter(IdNotFoundError("Parking",parking.parking_id))
    event = {'parking_id': parking_id, 'user': user.__dict__, 'office_id': office_id}

    result = delete_parking_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Parking id:'"+ parking.parking_id +"' not found"})
    

def test__delete_parking_controller__raise_PermissionsError(mocked_parking_deleter, user_factory):
    parking_id=Faker().uuid4()
    office_id=Faker().uuid4()
    user = user_factory()
    mocked_parking_deleter(PermissionsError("delete a parking"))
    event = {'parking_id': parking_id, 'user': user.__dict__, 'office_id': office_id}
    result = delete_parking_controller(event)
    assert result['status_code'] == HTTPStatus.UNAUTHORIZED
    assert result['body'] == json.dumps({'message': "You don't have permissions: <delete a parking>"})
    

def test__delete_parking_controller__raise_DomainError(mocked_parking_deleter, user_factory):
    office_id=Faker().uuid4()
    parking_id=Faker().uuid4()
    user = user_factory()
    mocked_parking_deleter(DomainError("An external error ocurred"))
    event = {'parking_id': parking_id, 'user': user.__dict__, 'office_id': office_id}
    result = delete_parking_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    
import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.parkings.application.parking_getter import ParkingGetter
from desk_reservation.parkings.infrastructure.controllers.get_parking import get_parking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError



@pytest.fixture(name='mocked_parking_getter')
def _mocked_library(mocker) -> Callable:
    def _create_parking_getter(parking_getter: any) -> None:
        mocker.patch('desk_reservation.parkings.infrastructure.controllers.get_parking.parking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(ParkingGetter, 'execute',
                            side_effect=parking_getter)
    return _create_parking_getter


def test__return_parking_when_parking_id_exist(mocked_parking_getter, mocker, parking_factory):
    parking = parking_factory()
    mocked_parking_getter(mocker.Mock(return_value=parking))

    result = get_parking_controller({'parking_id': parking.parking_id})
    assert result['status_code'] == HTTPStatus.FOUND
    assert result['body'] == json.dumps(parking.__dict__, default=str)
    
    
def test__return_raise_idnotfound_when_parking_id_doesnt_exist(mocked_parking_getter, mocker, parking_factory):
    parking = parking_factory()
    mocked_parking_getter(IdNotFoundError("Parking",parking.parking_id))

    result = get_parking_controller({'parking_id': parking.parking_id})
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Parking id:'"+ parking.parking_id +"' not found"})


def test__return_raise_DomainError(mocked_parking_getter, mocker, parking_factory):
    parking = parking_factory()
    mocked_parking_getter(DomainError("An external error ocurred"))

    result = get_parking_controller({'parking_id': parking.parking_id})
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    
from email.policy import default
import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.parkings.application.parking_finder import ParkingFinder
from desk_reservation.parkings.infrastructure.controllers.find_parking import find_parking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError



@pytest.fixture(name='mocked_parking_finder')
def _mocked_library(mocker) -> Callable:
    def _create_parking_finder(parking_finder: any) -> None:
        mocker.patch('desk_reservation.parkings.infrastructure.controllers.find_parking.parking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(ParkingFinder, 'execute',
                            side_effect=parking_finder)
    return _create_parking_finder


def test__find_parking_controller__return_parkings(mocked_parking_finder, mocker, parking_factory):
    parkings = [parking_factory() for _ in range(3)]
    mocked_parking_finder(mocker.Mock(return_value=parkings))

    event = {"queryStringParameters": {"filters":json.dumps([])}}
    result = find_parking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([ob.__dict__ for ob in parkings], default=str)
    
def test__find_parking_controller__dont_return_parkings(mocked_parking_finder, mocker, parking_factory):
    mocked_parking_finder(mocker.Mock(return_value=[]))
    event = {"queryStringParameters": {"filters":json.dumps([])}}
    result = find_parking_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([])
    

def test__find_parking_controller__raise_DomainError(mocked_parking_finder, mocker, parking_factory):
    mocked_parking_finder(DomainError("An external error ocurred"))

    event = {"queryStringParameters": {"filters":json.dumps([])}}
    result = find_parking_controller(event)
    assert result['status_code'] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result['body'] == json.dumps({'message': "An external error ocurred"})
    

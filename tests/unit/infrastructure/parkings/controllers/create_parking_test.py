import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.parkings.application.parking_creator import ParkingCreator
from desk_reservation.parkings.infrastructure.controllers.create_parking import create_parking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name='mocked_parking_creator')
def _mocked_library(mocker) -> Callable:
    def _create_parking_creator(parking_creator: any) -> None:
        mocker.patch('desk_reservation.parkings.infrastructure.controllers.create_parking.parking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(ParkingCreator, 'execute',
                            side_effect=parking_creator)
    return _create_parking_creator


def test__create_parking_controller__return_parking(mocked_parking_creator, mocker, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    mocked_parking_creator(mocker.Mock(return_value=parking))
    event = {"body": json.dumps(
        {**parking.__dict__, 'user_id': user.google_id, }, default=str)}

    result = create_parking_controller(event)
    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(parking.__dict__, default=str)


def test__create_parking_controller__raise_PermissionsError(mocked_parking_creator, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    mocked_parking_creator(PermissionsError("create a parking"))
    event = {"body": json.dumps(
        {**parking.__dict__, 'user_id': user.google_id, }, default=str)}

    result = create_parking_controller(event)
    assert result['status_code'] == HTTPStatus.UNAUTHORIZED
    assert result['body'] == json.dumps(
        {'message': "You don't have permissions: <create a parking>"})


def test__create_parking_controller__raise_NameAlreadyExistsError(mocked_parking_creator, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    mocked_parking_creator(NameAlreadyExistsError("Parking", parking.name))
    event = {"body": json.dumps(
        {**parking.__dict__, 'user_id': user.google_id, }, default=str)}

    result = create_parking_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps(
        {'message': "Cannot create a new <Parking>, Name: " + parking.name + " already exists"})


def test__create_parking_controller__raise_ValidationError(mocked_parking_creator, mocker, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    parking_dict = parking.__dict__
    del parking_dict['parking_id']
    mocked_parking_creator(mocker.Mock)

    event = {"body": json.dumps(
        {**parking.__dict__, 'user_id': user.google_id, }, default=str)}
    result = create_parking_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps(
        {'message': "Check parking attributes"})


def test__create_parking_controller__raise_DomainError(mocked_parking_creator, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    mocked_parking_creator(DomainError("An external error ocurred"))

    event = {"body": json.dumps(
        {**parking.__dict__, 'user_id': user.google_id, }, default=str)}
    result = create_parking_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps(
        {'message': "An external error ocurred"})

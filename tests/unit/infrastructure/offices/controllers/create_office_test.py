import json
from unittest.mock import patch
import pytest
from faker import Faker
from http import HTTPStatus
from typing import Callable

from desk_reservation.offices.application.office_creator import OfficeCreator
from desk_reservation.offices.infrastructure.controllers.create_office import create_office_controller
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError


@pytest.fixture(name='mocked_office_creator')
def _mocked_library(mocker) -> Callable:
    def _create_office_creator(office_creator: any) -> None:
        mocker.patch('desk_reservation.offices.infrastructure.controllers.create_office.office_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(OfficeCreator, 'execute',
                            side_effect=office_creator)
    return _create_office_creator


def test__return_valid_response_when_office_is_created(mocked_office_creator, mocker, office_factory):
    office = office_factory()
    event = {"body":json.dumps({**office.__dict__,"user_id":Faker().uuid4()}, default=str)}
    mocked_office_creator(mocker.Mock(return_value=office.__dict__))
    result = create_office_controller(event)
    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(office.__dict__, default=str)


def test__return_exeption_response_when_office_is_not_created(mocked_office_creator, office_factory):
    office = office_factory()
    event = {"body":json.dumps({**office.__dict__,"user_id":Faker().uuid4()}, default=str)}
    mocked_office_creator(BadRequestError('field office_id is required'))

    result = create_office_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': 'field office_id is required'})
    
    


import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.offices.application.office_deleter import OfficeDeleter
from desk_reservation.offices.infrastructure.controllers.delete_office import delete_office_controller


@pytest.fixture(name='mocked_office_deleter')
def _mocked_library(mocker) -> Callable:
    def _create_office_deleter(office_creator: any) -> None:
        mocker.patch('desk_reservation.offices.infrastructure.controllers.delete_office.office_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(OfficeDeleter, 'execute',
                            side_effect=office_creator)
    return _create_office_deleter


def test__return_true_when_office_is_deleted(mocked_office_deleter, mocker):
    office_id = Faker().uuid4()
    mocked_office_deleter(mocker.Mock(return_value=True))

    result = delete_office_controller({'office_id': office_id, 'user_id': Faker().uuid4()})
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] is json.dumps(None)


def test__return_false_when_office_is_deleted(mocked_office_deleter, mocker):
    office_id = Faker().uuid4()
    mocked_office_deleter(mocker.Mock(return_value=False))

    result = delete_office_controller({'office_id': office_id, 'user_id': Faker().uuid4()})
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] is json.dumps(None)
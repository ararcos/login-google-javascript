import json
import pytest
from faker import Faker
from typing import Callable
from http import HTTPStatus

from desk_reservation.offices.infrastructure.controllers.update_office import update_office_controller
from desk_reservation.offices.application import OfficeUpdater


@pytest.fixture(name='mocked_office_updater')
def _mocked_library(mocker) -> Callable:
    def _create_office_updater(office_creator: any) -> None:
        mocker.patch('desk_reservation.offices.infrastructure.controllers.update_office.office_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(OfficeUpdater, 'execute',
                            side_effect=office_creator)
    return _create_office_updater


def test__return_office_when_office_id_exist_an_updated_correctly(mocked_office_updater, mocker, office_factory):
    office = office_factory()
    event =  office.__dict__ | {'user_id': Faker().uuid4()}
    mocked_office_updater(mocker.Mock(return_value=office))

    result = update_office_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(office.__dict__, default=str     )


def test__return_not_found_when_office_id_not_exist(mocked_office_updater, mocker, office_factory):
    office = office_factory()
    event =  office.__dict__ | {'user_id': Faker().uuid4()}
    mocked_office_updater(mocker.Mock(return_value=None))

    result = update_office_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] is json.dumps(None)
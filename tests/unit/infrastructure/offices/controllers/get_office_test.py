import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker

from desk_reservation.offices.application import OfficeFinderOne
from desk_reservation.offices.infrastructure.controllers.get_office import get_office_controller


@pytest.fixture(name='mocked_office_finder_one')
def _mocked_library(mocker) -> Callable:
    def _create_office_finder_one(office_creator: any) -> None:
        mocker.patch('desk_reservation.offices.infrastructure.controllers.get_office.office_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(OfficeFinderOne, 'execute',
                            side_effect=office_creator)
    return _create_office_finder_one


def test__return_office_when_office_id_exist(mocked_office_finder_one, mocker, office_factory):
    office = office_factory()
    mocked_office_finder_one(mocker.Mock(return_value=office))

    result = get_office_controller({'office_id': office.office_id})
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(office.__dict__, default=str)


def test__return_not_found_when_office_id_not_exist(mocked_office_finder_one, mocker):
    mocked_office_finder_one(mocker.Mock(return_value=None))

    result = get_office_controller({'office_id': Faker().uuid4()})
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] is json.dumps(None)
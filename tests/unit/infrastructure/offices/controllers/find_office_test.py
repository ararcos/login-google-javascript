import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.offices.application import OfficeFinder
from desk_reservation.offices.infrastructure.controllers.find_offices import find_offices_controller


@pytest.fixture(name='mocked_office_finder')
def _mocked_library(mocker) -> Callable:
    def _create_office_finder(office_creator: any) -> None:
        mocker.patch('desk_reservation.offices.infrastructure.controllers.find_offices.office_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(OfficeFinder, 'execute',
                            side_effect=office_creator)
    return _create_office_finder


def test__return_list_when_office_has_data(mocked_office_finder, mocker, office_factory):
    offices = [office_factory() for _ in range(3)]
    mocked_office_finder(mocker.Mock(return_value=offices))

    event = {}
    result = find_offices_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([office.__dict__ for office in offices], default=str)


def test__return_empty_list_when_office_has_not_data(mocked_office_finder, mocker):
    offices = []
    mocked_office_finder(mocker.Mock(return_value=offices))

    event = {}
    result = find_offices_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(offices)
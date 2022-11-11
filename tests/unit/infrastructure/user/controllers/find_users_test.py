from http import HTTPStatus
import json
import pytest
from typing import Callable

from desk_reservation.users.application.user_finder import UserFinder
from desk_reservation.users.infrastructure.controllers.find_user import find_user_controller


@pytest.fixture(name='mocked_user_finder')
def _mocked_library(mocker) -> Callable:
    def _create_user_finder(user_finder: any) -> None:
        mocker.patch('desk_reservation.users.infrastructure.controllers.find_user.user_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(UserFinder, 'execute',
                            side_effect=user_finder)
    return _create_user_finder


def test__return_list_when_users_has_data(mocked_user_finder, mocker, user_factory):
    users = [user_factory() for _ in range(3)]
    mocked_user_finder(mocker.Mock(return_value=users))

    event = {"queryStringParameters": {"filters":json.dumps([])}}
    result = find_user_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([ob.__dict__ for ob in users])


def test__return_empty_list_when_users_has_not_data(mocked_user_finder, mocker):
    users = []
    mocked_user_finder(mocker.Mock(return_value=users))
    event = {"queryStringParameters": {"filters":json.dumps([])}}
    result = find_user_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps([])

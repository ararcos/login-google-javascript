from http import HTTPStatus
import json
import pytest
from faker import Faker
from typing import Callable

from desk_reservation.users.application.user_getter import UserGetter
from desk_reservation.users.infrastructure.controllers.get_user import get_user_controller


@pytest.fixture(name='mocked_user_getter')
def _mocked_library(mocker) -> Callable:
    def _create_user_getter(user_getter: any) -> None:
        mocker.patch('desk_reservation.users.infrastructure.controllers.get_user.user_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(UserGetter, 'execute',
                            side_effect=user_getter)
    return _create_user_getter


def test__return_not_found_when_user_id_not_exist(mocked_user_getter, mocker):
    mocked_user_getter(mocker.Mock(return_value=None))
    event = {'pathParameters': {'user_id':  Faker().uuid4()}}
    result = get_user_controller(event)
    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps(None)


def test__return_true_when_getting_user(mocked_user_getter, mocker, user_factory):
    google_id = Faker().uuid4()
    user = user_factory()
    mocked_user_getter(mocker.Mock(return_value=user))
    event = {'pathParameters': {'user_id': google_id}}

    result = get_user_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(user.__dict__)

from http import HTTPStatus
import json
import pytest
from typing import Callable
from faker import Faker
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.users.application.user_editor import UserEditor

from desk_reservation.users.application.user_getter import UserGetter
from desk_reservation.users.infrastructure.controllers.update_user import update_user_controller


@pytest.fixture(name='mocked_user_setter')
def _mocked_library(mocker) -> Callable:
    def _create_user_setter(user_setter: any) -> None:
        mocker.patch('desk_reservation.users.infrastructure.controllers.update_user.user_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(UserEditor, 'execute',
                            side_effect=user_setter)
    return _create_user_setter


def test__return_exception_validation_error_response_when_user_is_not_created(user_factory, mocked_user_setter, mocker):
    user = user_factory()
    user_dict = user.__dict__
    user_dict.pop("email")
    event = {"body": json.dumps({**user_dict, "google_id": Faker().uuid4()})}
    mocked_user_setter(mocker.Mock(return_value=user))

    result = update_user_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check User Attributes"})


def test__return_true_when_editing_user(mocked_user_setter, mocker, user_factory):
    user = user_factory()
    event = {"body": json.dumps({**user.__dict__, 'google_id': Faker().uuid4()})}
    mocked_user_setter(mocker.Mock(return_value=user))

    result = update_user_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(user.__dict__)


def test__raise_exception_when_not_having_permission_to_update_user(mocked_user_setter, user_factory):
    user = user_factory()
    event = {"body": json.dumps({
        **user.__dict__, "google_id": Faker().uuid4()
    })}
    mocked_user_setter(PermissionsError("Update a User"))

    result = update_user_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({
        "message": "You don't have permissions: <Update a User>"})

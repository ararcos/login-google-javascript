from http import HTTPStatus
import json
from typing import Callable
import pytest
from faker import Faker
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.users.application.user_deleter import UserDeleter
from desk_reservation.users.infrastructure.controllers.delete_user import delete_user_controller


@pytest.fixture(name='mocked_user_deleter')
def _mocked_library(mocker) -> Callable:
    def _create_user_deleter(user_deleter: any) -> None:
        mocker.patch('desk_reservation.users.infrastructure.controllers.delete_user.user_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(UserDeleter, 'execute',
                            side_effect=user_deleter)
    return _create_user_deleter


def test__delete_user_controller__raise_PermissionsError(mocked_user_deleter):
    mocked_user_deleter(PermissionsError("delete a user"))
    event = {'google_id': Faker().uuid4(), 'user_id': Faker().uuid4()}

    result = delete_user_controller(event)
    assert result['status_code'] == HTTPStatus.FORBIDDEN
    assert result['body'] == json.dumps({
        'message': "You don't have permissions: <delete a user>"})

def test__delete_user_controller__raise_DomainError(mocked_user_deleter):
    mocked_user_deleter(DomainError("An external error ocurred"))
    event = {'google_id': Faker().uuid4(), 'user_id': Faker().uuid4()}

    result = delete_user_controller(event)
    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == json.dumps({'message': "An external error ocurred"})


def test__return_true_when_user_is_deleted(mocked_user_deleter, mocker):
    google_id = Faker().uuid4()
    user_id = Faker().uuid4()
    mocked_user_deleter(mocker.Mock(return_value=True))
    event = {'google_id': google_id, 'user_id': user_id}

    result = delete_user_controller(event)
    assert result['status_code'] == HTTPStatus.OK
    assert result['body'] == json.dumps(None)

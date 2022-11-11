import json
import pytest
from http import HTTPStatus
from typing import Callable
from faker import Faker
from pydantic import ValidationError

from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.users.application.user_creator import UserCreator
from desk_reservation.users.domain.exceptions.incorrect_domain_error import IncorrectDomainError
from desk_reservation.users.infrastructure.controllers.create_user import create_user_controller


@pytest.fixture(name='mocked_user_creator')
def _mocked_library(mocker) -> Callable:
    def _create_user_creator(user_creator: any) -> None:
        mocker.patch('desk_reservation.users.infrastructure.controllers.create_user.user_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(UserCreator, 'execute',
                            side_effect=user_creator)
    return _create_user_creator


def test__return_exception_validation_error_response_when_user_is_not_created(user_factory, mocked_user_creator, mocker):
    user = user_factory()
    user_dict = user.__dict__
    user_dict.pop("email")
    event = {"body":json.dumps({**user_dict,"user_id":Faker().uuid4()}, default=str)}
    mocked_user_creator(mocker.Mock(return_value=user))

    result = create_user_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check User Attributes"})


def test__return_valid_response_when_user_is_created(mocked_user_creator, mocker, user_factory):
    user = user_factory()
    event = {"body":json.dumps({**user.__dict__,"user_id":Faker().uuid4()}, default=str)}
    mocked_user_creator(mocker.Mock(return_value=user))
    result = create_user_controller(event)
    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(user.__dict__)


def test__create_user_controller__raise_PermissionsError(mocked_user_creator, mocker, user_factory):
    user = user_factory()
    mocked_user_creator(PermissionsError("create a user"))
    event = {"body":json.dumps({**user.__dict__,'google_id': Faker().uuid4(),"user_id":Faker().uuid4()}, default=str)}

    result = create_user_controller(event)
    assert result['status_code'] == HTTPStatus.FORBIDDEN
    assert result['body'] == json.dumps({
        'message': "You don't have permissions: <create a user>"})


def test__create_user_controller__raise_IncorrectDomainError(mocked_user_creator, user_factory):
    user = user_factory(
        email='asd@gmail.com'
    )
    mocked_user_creator(IncorrectDomainError())
    event = {"body":json.dumps({**user.__dict__,'google_id': Faker().uuid4(),"user_id":Faker().uuid4()}, default=str)}

    result = create_user_controller(event)
    assert result['status_code'] == HTTPStatus.CONFLICT
    assert result['body'] == json.dumps({
        'message': 409,
        'details': "The Domain must be @ioet.com"
})

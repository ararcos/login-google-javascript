from http import HTTPStatus
import json
from typing import Callable
from faker import Faker
import pytest

from desk_reservation.desks.application.desk_creator import DeskCreator
from desk_reservation.desks.infrastructure.controllers import create_desk_controller
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name="mocked_desk_creator")
def _mocked_library(mocker) -> Callable:
    def _create_desk_creator(desk_creator: any) -> None:
        mocker.patch(
            "desk_reservation.desks.infrastructure.controllers.create_desk.desk_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(DeskCreator, "execute", side_effect=desk_creator)

    return _create_desk_creator


def test__return_valid_response_when_desk_is_created(
    mocked_desk_creator, mocker, desk_factory
):
    desk = desk_factory()
    event = {"body": json.dumps({**desk.__dict__ ,"user_id": Faker().uuid4()}, default=str)}
    mocked_desk_creator(mocker.Mock(return_value=desk))
    result = create_desk_controller(event)
    assert result["status_code"] == HTTPStatus.CREATED
    assert result["body"] == json.dumps(desk.__dict__, default=str)

def test__return_permission_exception_response_when_desk_is_not_created(
    mocked_desk_creator, desk_factory
):
    desk = desk_factory()
    event = {"body": json.dumps({**desk.__dict__ ,"user_id": Faker().uuid4()}, default=str)}
    mocked_desk_creator(PermissionsError("Create a Desk"))

    result = create_desk_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({"message": "You don't have permissions: <Create a Desk>"})

def test__return_exception_validation_error_response_when_desk_is_not_created(
    desk_factory, mocked_desk_creator, mocker
):
    desk = desk_factory()
    desk_dict = desk.__dict__
    desk_dict.pop("desk_id")
    event = {"body": json.dumps({**desk.__dict__ ,"user_id": Faker().uuid4()}, default=str)}
    mocked_desk_creator(mocker.Mock(return_value=desk))

    result = create_desk_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Desk Attributes"})

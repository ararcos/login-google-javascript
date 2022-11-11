import json
from typing import Callable
from http import HTTPStatus
import pytest
from faker import Faker

from desk_reservation.desks.application.desk_deleter import DeskDeleter
from desk_reservation.desks.infrastructure.controllers.delete_desk import (
    delete_desk_controller,
)
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name="mocked_desk_deleter")
def _mocked_library(mocker) -> Callable:
    def _create_desk_deleter(desk_creator: any) -> None:
        mocker.patch(
            "desk_reservation.desks.infrastructure.controllers.delete_desk.desk_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(DeskDeleter, "execute", side_effect=desk_creator)

    return _create_desk_deleter


def test__return_true_when_desk_is_deleted(mocked_desk_deleter, mocker):
    desk_id = Faker().uuid4()
    mocked_desk_deleter(mocker.Mock(return_value=True))

    result = delete_desk_controller({"desk_id": desk_id, "user_id": Faker().uuid4()})
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(None)


def test__return_false_when_desk_is_deleted(mocked_desk_deleter, mocker):
    desk_id = Faker().uuid4()
    mocked_desk_deleter(mocker.Mock(return_value=False))

    result = delete_desk_controller({"desk_id": desk_id, "user_id": Faker().uuid4()})
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(None)


def test__return_permission_exception_response_when_desk_is_not_deleted(
    mocked_desk_deleter, desk_factory
):
    desk = desk_factory()
    event = desk.__dict__ | {"user_id": Faker().uuid4()}
    mocked_desk_deleter(PermissionsError("Delete a Desk"))

    result = delete_desk_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({"message": "You don't have permissions: <Delete a Desk>"})

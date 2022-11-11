import json
from typing import Callable
from http import HTTPStatus
import pytest
from faker import Faker

from desk_reservation.desks.infrastructure.controllers.update_desk import (
    update_desk_controller,
)
from desk_reservation.desks.application import DeskUpdater
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name="mocked_desk_updater")
def _mocked_library(mocker) -> Callable:
    def _create_desk_updater(desk_creator: any) -> None:
        mocker.patch(
            "desk_reservation.desks.infrastructure.controllers.update_desk.desk_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(DeskUpdater, "execute", side_effect=desk_creator)

    return _create_desk_updater


def test__return_desk_when_desk_id_exist_an_updated_correctly(
    mocked_desk_updater, mocker, desk_factory
):
    desk = desk_factory()
    event = desk.__dict__ | {"user_id": Faker().uuid4()}
    mocked_desk_updater(mocker.Mock(return_value=desk))

    result = update_desk_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(desk.__dict__, default=str)


def test__return_not_found_when_desk_id_not_exist(
    mocked_desk_updater, mocker, desk_factory
):
    desk = desk_factory()
    event = desk.__dict__ | {"user_id": Faker().uuid4()}
    mocked_desk_updater(mocker.Mock(return_value=None))

    result = update_desk_controller(event)
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(None)


def test__return_permission_exception_response_when_desk_is_not_updated(
    mocked_desk_updater, desk_factory
):
    desk = desk_factory()
    event = desk.__dict__ | {"user_id": Faker().uuid4()}
    mocked_desk_updater(PermissionsError("Update a Desk"))

    result = update_desk_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({"message": "You don't have permissions: <Update a Desk>"})

def test__return_exception_validation_error_response_when_desk_is_not_updated(
    desk_factory, mocked_desk_updater, mocker
):
    desk = desk_factory()
    desk_dict = desk.__dict__
    desk_dict.pop("desk_id")
    event = {**desk_dict, "user_id" : Faker().uuid4()}
    mocked_desk_updater(mocker.Mock(return_value=desk))

    result = update_desk_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Desk Attributes"})

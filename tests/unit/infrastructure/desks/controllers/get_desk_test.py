import json
from typing import Callable
from http import HTTPStatus
from faker import Faker
import pytest

from desk_reservation.desks.application import FinderById
from desk_reservation.desks.infrastructure.controllers.get_desk import (
    get_desk_controller,
)


@pytest.fixture(name="mocked_desk_finder_one")
def _mocked_library(mocker) -> Callable:
    def _create_desk_finder_one(desk_creator: any) -> None:
        mocker.patch(
            "desk_reservation.desks.infrastructure.controllers.get_desk.desk_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(FinderById, "execute", side_effect=desk_creator)

    return _create_desk_finder_one


def test__return_desk_when_desk_id_exist(mocked_desk_finder_one, mocker, desk_factory):
    desk = desk_factory()
    mocked_desk_finder_one(mocker.Mock(return_value=desk))

    result = get_desk_controller({"desk_id": desk.desk_id})
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(desk.__dict__, default=str)


def test__return_not_found_when_desk_id_not_exist(mocked_desk_finder_one, mocker):
    mocked_desk_finder_one(mocker.Mock(return_value=None))

    result = get_desk_controller({"desk_id": Faker().uuid4()})
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(None)

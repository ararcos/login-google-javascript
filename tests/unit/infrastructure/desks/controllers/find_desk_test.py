import json
from typing import Callable
from http import HTTPStatus
import pytest

from desk_reservation.desks.application import DeskFinder
from desk_reservation.desks.infrastructure.controllers.find_desks import (
    find_desks_controller,
)


@pytest.fixture(name="mocked_desk_finder")
def _mocked_library(mocker) -> Callable:
    def _create_desk_finder(desk_creator: any) -> None:
        mocker.patch(
            "desk_reservation.desks.infrastructure.controllers.find_desks.desk_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(DeskFinder, "execute", side_effect=desk_creator)

    return _create_desk_finder


def test__return_list_when_desk_has_data(mocked_desk_finder, mocker, desk_factory):
    desks = [desk_factory() for _ in range(3)]
    mocked_desk_finder(mocker.Mock(return_value=desks))

    result = find_desks_controller({},{})
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps([ob.__dict__ for ob in desks], default=str)


def test__return_empty_list_when_desk_has_not_data(mocked_desk_finder, mocker):
    desks = []
    mocked_desk_finder(mocker.Mock(return_value=desks))

    result = find_desks_controller({},{})
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(desks)

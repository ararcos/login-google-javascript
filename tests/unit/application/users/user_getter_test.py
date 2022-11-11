import pytest
from faker import Faker

from desk_reservation.users.application.user_getter import UserGetter


def test__get_user_return_user_when_id_was_found(mocker, user_factory):
    user= user_factory()
    google_id = Faker().uuid4()
    user_service = mocker.Mock(
        get_user=mocker.Mock(
            return_value = user
        )
    )
    user_getter= UserGetter(user_service=user_service)
    result = user_getter.execute(google_id)
    assert result == user

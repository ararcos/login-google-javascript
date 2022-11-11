import pytest
from faker import Faker
from desk_reservation.users.application.user_editor import UserEditor


def test___user_updater_return_user_when_having_permission_to_update_user(mocker, user_factory):
    google_id = Faker().uuid4()
    user = user_factory()
    user_service = mocker.Mock(
        edit_user=mocker.Mock(return_value=user)
    )
    user_editor = UserEditor(user_service=user_service)
    result = user_editor.execute(google_id=google_id, user=user)
    assert result == user

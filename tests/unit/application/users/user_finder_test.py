import pytest

from desk_reservation.users.application import UserFinder


def test___user_finder_was_called_correctly(mocker):
    criteria = mocker.Mock()
    user_service = mocker.Mock(
        find_user=mocker.Mock()
    )
    user_editor = UserFinder(user_service=user_service)
    user_editor.execute(criteria)
    user_service.find_user.assert_called_with(criteria)

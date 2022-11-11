import pytest
from faker import Faker

from desk_reservation.users.application.user_creator import UserCreator

def test___user_creator_return_true_when_user_was_created_correctly(mocker, user_factory):
    user= user_factory()
    google_id= Faker().uuid4()
    user_service= mocker.Mock(
        create_user=mocker.Mock(return_value=user)
    )
    user_creator= UserCreator(user_service=user_service)
    result = user_creator.execute(google_id=google_id, user=user)
    assert result == user

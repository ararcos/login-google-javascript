import pytest
from faker import Faker
from desk_reservation.users.application.user_deleter import UserDeleter

def test__return_false_when_there_was_a_problem_deleting_a_user (mocker):
    google_id= Faker().uuid4()
    user_id = Faker().uuid4()
    user_service= mocker.Mock(
        delete_user=mocker.Mock(return_value=False)
    )
    user_deleter = UserDeleter(user_service=user_service)
    result =  user_deleter.execute(google_id=google_id, user_id=user_id)
    assert result == False

def test___user_deleter_return_true_when_the_google_id_exist_and_have_permissions(mocker):
    google_id= Faker().uuid4()
    user_id = Faker().uuid4()
    user_service= mocker.Mock(
        delete_user=mocker.Mock(return_value=True)
    )
    user_deleter = UserDeleter(user_service=user_service)
    result =  user_deleter.execute(google_id=google_id, user_id=user_id)
    assert result == True

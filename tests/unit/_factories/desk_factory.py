from datetime import datetime, timedelta
from faker import Faker
import pytest

from desk_reservation.desks.domain.entities.desk import Desk

faker = Faker()


@pytest.fixture
def desk_factory():
    def _factory(**kwargs):
        args = {
            **{
                "desk_id": faker.uuid4(),
                "desk_name": faker.pystr(),
                "top_pixel": faker.random_digit(),
                "left_pixel": faker.random_digit(),
                "width": faker.random_digit(),
                "height": faker.random_digit(),
                "seats_list": [faker.uuid4() for _ in range(1, 5)],
                "office_id": faker.uuid4(),
                "created_at": datetime.today(),
                "updated_at": datetime.today() + timedelta(hours=1),
                "updated_by": faker.uuid4(),
                "deleted_at": datetime.today() + timedelta(hours=1),
                "deleted_by": faker.uuid4(),
            },
            **kwargs,
        }
        return Desk(**args)

    return _factory

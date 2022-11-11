from datetime import datetime, timedelta
from typing import List, Union

import pytest
from faker import Faker

from desk_reservation.offices.domain import Office

faker = Faker()


@pytest.fixture
def office_factory():
    def _factory(**kwargs):
        args = {
            **{
                'office_id': faker.uuid4(),
                'name': faker.name(),
                'managers': [faker.pystr() for _ in range(3)],
                'desks': [faker.pystr() for _ in range(3)],
                'seats': [faker.pystr() for _ in range(3)],
                'parkings': [faker.pystr() for _ in range(3)],
                'floor_image': faker.image_url(),
                'created_at': faker.future_datetime(),
            },
            **kwargs
        }
        return Office(**args)

    return _factory

from http import HTTPStatus

#pylint: disable=R0801

from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    user_service_factory
    )
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.users.application.user_getter import UserGetter

# pylint: disable=W0613 W0703
def get_user_controller(event, context=None, callback=None):
    user_service = user_service_factory()
    google_id = event['pathParameters']["user_id"]
    user_getter = UserGetter(user_service)
    try:
        result = user_getter.execute(google_id=google_id)
        response = (HTTPStatus.OK, result.__dict__) if result else(
            HTTPStatus.NOT_FOUND, None)
        return ControllerResponse(
            status_code=response[0],
            body=response[1]
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__

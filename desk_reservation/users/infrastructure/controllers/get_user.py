from http import HTTPStatus
#pylint: disable=R0801

from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.controllers import message_response
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.infrastructure.dependency_injection import user_service_factory
from ...application.user_getter import UserGetter


def get_user_controller(event):
    user_service = user_service_factory()
    google_id = event['google_id']
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

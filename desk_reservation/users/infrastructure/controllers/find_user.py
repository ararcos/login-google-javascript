from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers.filters_controller import filters_controller

#pylint: disable=R0801

from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    user_service_factory
    )
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.users.application.user_finder import UserFinder
from desk_reservation.shared.domain.exceptions.domain_error import DomainError

# pylint: disable=W0613
def find_user_controller(event, context=None, callback=None):
    user_service = user_service_factory()
    user_finder = UserFinder(user_service)
    params = event.get('queryStringParameters')
    try:
        criteria = filters_controller(params,False)
        result = user_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__
    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__

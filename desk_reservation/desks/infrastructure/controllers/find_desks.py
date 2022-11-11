from http import HTTPStatus


from desk_reservation.desks.application.desk_finder import DeskFinder
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    desk_service_factory
    )
from desk_reservation.shared.infrastructure.controllers import filters_controller

# pylint: disable=W0613 duplicate-code
def find_desks_controller(event, context):
    desk_service = desk_service_factory()
    desk_finder = DeskFinder(desk_service)
    params = event.get('queryStringParameters')
    populate = params.get('populate', False) if params else False
    try:
        criteria = filters_controller(params)
        result = desk_finder.execute(criteria, populate)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__

    except DomainError as error:
        response = filters_controller(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=response
        ).__dict__

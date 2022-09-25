from http import HTTPStatus

from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.infrastructure.controllers import message_response
from ...application.seat_getter import SeatGetter
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import seat_service_factory
from ....shared.infrastructure.controllers import ControllerResponse


def get_seat_controller(event):
    seat_service = seat_service_factory()
    seat_id = event.pop('seat_id')
    seat_getter = SeatGetter(seat_service)
    try:
        result = seat_getter.execute(seat_id=seat_id)
        return ControllerResponse(
            status_code=HTTPStatus.FOUND, body=result.__dict__).__dict__

    except IdNotFoundError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND, body=response).__dict__

    except DomainError as error:
        response = {
            'message': error.args[0]}
        if len(error.args) == 2:
            response['details'] = error.args[1]

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response).__dict__

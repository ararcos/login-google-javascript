from http import HTTPStatus

from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ...application.seat_deleter import SeatDeleter
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import seat_service_factory
from ....shared.infrastructure.controllers import ControllerResponse


def delete_seat_controller(event):
    seat_service = seat_service_factory()
    user_id = event.pop('user_id')
    seat_id = event.pop('seat_id')
    office_id = event.pop('office_id')
    seat_deleter = SeatDeleter(seat_service)
    try:
        result = seat_deleter.execute(
            user_id=user_id, seat_id=seat_id, office_id=office_id)
        return ControllerResponse(
            status_code=HTTPStatus.OK,
            body=result.__dict__).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            body=response).__dict__

    except IdNotFoundError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND,
            body=response).__dict__

    except DomainError as error:
        resp = {
            'message': error.args[0]
        }
        if len(error.args) == 2:
            resp['details'] = error.args[1]

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=resp).__dict__

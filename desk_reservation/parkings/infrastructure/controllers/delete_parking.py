from http import HTTPStatus

from ...application.parking_deleter import ParkingDeleter
from ....users.domain.entities.user import User
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import parking_service_factory
from ....shared.infrastructure.controllers import ControllerResponse


def delete_parking_controller(event):
    parking_service = parking_service_factory()
    parking_id = event['parking_id']
    office_id = event['office_id']
    try:
        user = User(**event['user'])
        parking_deleter = ParkingDeleter(parking_service)
        result = parking_deleter.execute(parking_id=parking_id, user=user, office_id=office_id)
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

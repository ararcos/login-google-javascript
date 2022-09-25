from http import HTTPStatus

from ...application.parking_getter import ParkingGetter
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.infrastructure.controllers import message_response
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import parking_service_factory
from ....shared.infrastructure.controllers import ControllerResponse


def get_parking_controller(event):
    parking_service = parking_service_factory()
    
    try:
        parking_id = event.pop('parking_id')
        parking_getter = ParkingGetter(parking_service)
        result = parking_getter.execute(parking_id=parking_id)
        return ControllerResponse(
            status_code=HTTPStatus.FOUND, body=result.__dict__).__dict__

    except IdNotFoundError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND, body=response).__dict__

    except (DomainError, KeyError) as error:
        response = {
            'message': error.args[0]}
        if len(error.args) == 2:
            response['details'] = error.args[1]

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response).__dict__

from http import HTTPStatus
import json
from pydantic.error_wrappers import ValidationError

from desk_reservation.parkings.application.parking_creator import ParkingCreator
from desk_reservation.parkings.domain.entities.parking import Parking
from desk_reservation.shared.domain.exceptions import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import parking_service_factory
from desk_reservation.shared.infrastructure.controllers import ControllerResponse



def create_parking_controller(event, context=None, callback=None):
    parking_service = parking_service_factory()
    try:
        body = json.loads(event["body"])
        user_id = body.pop('user_id')
        parking = Parking(**body)
        parking_creator = ParkingCreator(parking_service)
        result = parking_creator.execute(user_id=user_id, parking=parking)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED, body=result.__dict__).__dict__

    except ValidationError:
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body={'message':"Check parking attributes"}).__dict__ 

    except NameAlreadyExistsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body=response).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.UNAUTHORIZED, body=response).__dict__
    
    except DomainError as error:
        response = {'message': error.args[0]}
        if len(error.args) == 2:
            response['details'] = error.args[1]
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response).__dict__

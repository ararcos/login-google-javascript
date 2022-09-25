from http import HTTPStatus
from pydantic.error_wrappers import ValidationError

from ...application.parking_creator import ParkingCreator
from ...domain.entities.parking import Parking
from ....users.domain.entities.user import User
from ....shared.domain.exceptions import NameAlreadyExistsError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import parking_service_factory
from ....shared.infrastructure.controllers import ControllerResponse



def create_parking_controller(event):
    parking_service = parking_service_factory()
    try:
        user = User(**event['user'])
        parking = Parking(**event['parking'])
        parking_creator = ParkingCreator(parking_service)
        result = parking_creator.execute(user=user, parking=parking)
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

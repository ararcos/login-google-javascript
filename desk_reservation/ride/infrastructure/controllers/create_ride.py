from http import HTTPStatus
from pydantic import ValidationError
from ....shared.domain.exceptions import DomainError
from ....shared.infrastructure.dependency_injection import ride_service_factory
from ....shared.infrastructure import ControllerResponse, message_response
from ...application import RideCreator
from ...domain import Ride


def create_ride_controller(event):
    try:
        ride_service = ride_service_factory()
        ride = Ride(**event)
        ride_creator = RideCreator(ride_service)
        result = ride_creator.execute(
            ride_candidate=ride).__dict__
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result
        ).__dict__

    except (ValidationError, KeyError) :
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Ride Attributes"}
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__

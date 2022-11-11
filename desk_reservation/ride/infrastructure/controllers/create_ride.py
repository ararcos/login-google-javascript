from http import HTTPStatus
import json
from pydantic import ValidationError

from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure import ControllerResponse, message_response
from desk_reservation.ride.application import RideCreator
from desk_reservation.ride.domain import Ride


# pylint: disable=W0613
def create_ride_controller(event, context=None, callback=None):
    try:
        ride_service = ride_service_factory()
        body = json.loads(event["body"])
        ride = Ride(**body)
        ride_creator = RideCreator(ride_service)
        result = ride_creator.execute(
            ride_candidate=ride)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result.__dict__
        ).__dict__

    except (ValidationError, KeyError) as error:
        response = message_response(error.args)
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

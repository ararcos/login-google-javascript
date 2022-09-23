from desk_reservation.parkings.domain.services.parking_service import ParkingService
from ....users.domain.services.user_service import UserService
from ....ride.infrastructure.persistance import FirebaseRideRepository
from ....ride.domain.services.ride_service import RideService
from .. import FirebaseRepository
from ....desks.domain.services.desk_service import DeskService
from ....offices.domain.services.office_service import OfficeService
from ....seats.domain.services.seat_service import SeatService
from ....offices.infrastructure import FirebaseOfficeRepository
from ....bookings.domain.services import BookingService
from ....bookings.infrastructure.persistence import FirebaseBookingRepository
from ....users.infrastructure.persistence.firebase_user_repository import (
    FirebaseUserRepository)
from ....seats.infrastructure.persistance.firebase_seat_repository import (
    FirebaseSeatRepository)
from ....parkings.infrastructure.persistence.firebase_parking_repository import (
    FirebaseParkingRepository,
)
from ....desks.infrastructure.persistence.firebase_desk_repository import (
    FirebaseDeskRepository,
)


def booking_service_factory() -> BookingService:
    firebase_repository = FirebaseRepository()
    booking_repository = FirebaseBookingRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)
    return BookingService(
        booking_repository=booking_repository, user_repository=user_repository
    )


def seat_service_factory() -> SeatService:
    firebase_repository = FirebaseRepository()
    seat_repository = FirebaseSeatRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)
    office_repository = FirebaseOfficeRepository(firebase_repository)

    return SeatService(
        seat_repository=seat_repository,
        user_repository=user_repository,
        office_repository=office_repository
    )


def parking_service_factory() -> ParkingService:
    firebase_repository = FirebaseRepository()
    parking_repository = FirebaseParkingRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)
    office_repository = FirebaseOfficeRepository(firebase_repository)

    return ParkingService(
        parking_repository=parking_repository,
        user_repository=user_repository,
        office_repository=office_repository
    )


def office_service_factory() -> OfficeService:
    firebase_repository = FirebaseRepository()
    office_repository = FirebaseOfficeRepository(firebase_repository)
    seat_repository = FirebaseSeatRepository(firebase_repository)
    parking_repository = FirebaseParkingRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)

    return OfficeService(
        office_repository=office_repository,
        seat_repository=seat_repository,
        parking_repository=parking_repository,
        user_repository=user_repository,
    )


def desk_service_factory() -> DeskService:
    firebase_repository = FirebaseRepository()
    desk_repository = FirebaseDeskRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)
    office_repository = FirebaseOfficeRepository(firebase_repository)
    seat_repository = FirebaseSeatRepository(firebase_repository)
    return DeskService(
        desk_repository=desk_repository,
        user_repository=user_repository,
        office_repository=office_repository,
        seat_repository=seat_repository,
    )


def user_service_factory() -> UserService:
    firebase_repository = FirebaseRepository()
    user_repository = FirebaseUserRepository(firebase_repository)
    return UserService(user_repository=user_repository)


def ride_service_factory() -> RideService:
    firebase_repository = FirebaseRepository()
    ride_repository = FirebaseRideRepository(firebase_repository)
    user_repository = FirebaseUserRepository(firebase_repository)
    return RideService(ride_repository=ride_repository, user_repository=user_repository)

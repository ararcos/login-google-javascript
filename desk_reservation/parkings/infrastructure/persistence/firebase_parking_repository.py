from datetime import datetime
from typing import List, Optional

from ....shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ...domain import Parking, ParkingRepository


class FirebaseParkingRepository(ParkingRepository):
    def __init__(self, firebase_repository: FirebaseRepository):
        self.reference = firebase_repository.data_base.collection('parkings')

    
    def get(self, parking_id: str) -> Optional[Parking]:
        parking_ref = self.reference.document(parking_id)
        parking_data = parking_ref.get()
        if parking_data.exists:
            return Parking(**parking_data.to_dict())
        return None

    def create(self, parking: Parking) -> Parking:
        parking_ref = self.reference.document(parking.parking_id)
        parking_ref.set(parking.__dict__)
        return parking

    def update(self, parking: Parking) -> Optional[Parking]:
        parking_ref = self.reference.document(parking.parking_id)
        parking_data = parking_ref.get()
        if parking_data.exists:
            parking_ref.set(parking.__dict__)
            return parking
        return None

    def delete(self, parking_id: str) -> bool:
        parking_ref = self.reference.document(parking_id)
        parking_data = parking_ref.get()
        if parking_data.exists:
            parking_ref.update({'deleted_at': datetime.today()})
            return True
        return False
    
    def find(self, criteria: Criteria) -> List[Parking]:
        query = self.reference
        if criteria.filters:
            for _filter in criteria.filters:
                query = query.where(
                    _filter.field, _filter.operator.value, _filter.value)
        result = [Parking(**_doc.to_dict()) for _doc in query.get()]
        return result

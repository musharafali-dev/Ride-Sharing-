from abc import ABC, abstractmethod
import uuid
from typing import Optional, List
from app.domain.entities.vehicle import Vehicle

class VehicleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, vehicle_id: uuid.UUID) -> Optional[Vehicle]:
        pass

    @abstractmethod
    async def get_all(self, category: Optional[str] = None) -> List[Vehicle]:
        pass

    @abstractmethod
    async def save(self, vehicle: Vehicle) -> None:
        pass

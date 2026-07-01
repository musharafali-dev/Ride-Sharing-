from abc import ABC, abstractmethod
import uuid
from typing import Optional, List
from datetime import datetime
from app.domain.entities.booking import Booking

class BookingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, booking_id: uuid.UUID) -> Optional[Booking]:
        pass

    @abstractmethod
    async def get_by_customer_id(self, customer_id: uuid.UUID) -> List[Booking]:
        pass

    @abstractmethod
    async def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    async def check_availability(self, vehicle_id: uuid.UUID, start_time: datetime, end_time: datetime) -> bool:
        pass

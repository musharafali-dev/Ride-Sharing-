import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.domain.entities.vehicle import VehicleStatus
from app.domain.entities.booking import BookingStatus

class VehicleResponse(BaseModel):
    id: uuid.UUID
    category: str
    make: str
    model: str
    year: int
    color: str
    license_plate: str
    price_per_hour: float
    image_url: Optional[str] = None
    status: VehicleStatus

    class Config:
        from_attributes = True

class CreateBookingRequest(BaseModel):
    vehicle_id: uuid.UUID
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    vehicle_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    total_fare: float
    status: BookingStatus
    created_at: datetime
    vehicle: Optional[VehicleResponse] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

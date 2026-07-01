from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.vehicle import VehicleResponse

class BookingBase(BaseModel):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    tour_id: Optional[str] = None
    booking_type: str # ride, rental, tour
    start_time: datetime
    end_time: datetime
    total_amount: float

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: str
    customer_id: str
    status: str
    created_at: datetime
    vehicle: Optional[VehicleResponse] = None

    class Config:
        from_attributes = True

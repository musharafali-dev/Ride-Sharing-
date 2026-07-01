from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleBase(BaseModel):
    category: str # city_ride, car_rental, bike_rental, bus_coaster, luxury
    make: str
    model: str
    year: int
    color: str
    license_plate: str
    price_per_day: float
    price_per_hour: float
    seats: int
    transmission: Optional[str] = "automatic"
    fuel_type: Optional[str] = "petrol"
    image_url: Optional[str] = None
    is_available: Optional[bool] = True

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: str
    owner_id: str
    created_at: datetime

    class Config:
        from_attributes = True

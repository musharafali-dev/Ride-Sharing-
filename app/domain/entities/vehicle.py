from dataclasses import dataclass, field
from enum import Enum
import uuid

class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    MAINTENANCE = "maintenance"

@dataclass
class Vehicle:
    category: str  # "car", "van", "bike", "coaster"
    make: str
    model: str
    year: int
    color: str
    license_plate: str
    price_per_hour: float
    image_url: str
    status: VehicleStatus = VehicleStatus.AVAILABLE
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if not self.license_plate or len(self.license_plate.strip()) < 3:
            raise ValueError("Invalid license plate.")
        if self.price_per_hour <= 0:
            raise ValueError("Price per hour must be positive.")
        if self.category not in ["car", "van", "bike", "coaster"]:
            raise ValueError("Invalid vehicle category.")

    def book(self):
        if self.status != VehicleStatus.AVAILABLE:
            raise ValueError("Vehicle is not available for booking.")
        self.status = VehicleStatus.BOOKED

    def release(self):
        self.status = VehicleStatus.AVAILABLE

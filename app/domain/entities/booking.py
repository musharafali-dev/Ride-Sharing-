from dataclasses import dataclass, field
from enum import Enum
import uuid
from datetime import datetime

class BookingStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Booking:
    customer_id: uuid.UUID
    vehicle_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    total_fare: float
    status: BookingStatus = BookingStatus.PENDING
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time.")
        if self.total_fare < 0:
            raise ValueError("Total fare cannot be negative.")

    def activate(self):
        if self.status != BookingStatus.PENDING:
            raise ValueError("Can only activate pending bookings.")
        self.status = BookingStatus.ACTIVE

    def complete(self):
        if self.status != BookingStatus.ACTIVE:
            raise ValueError("Can only complete active bookings.")
        self.status = BookingStatus.COMPLETED

    def cancel(self):
        if self.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            raise ValueError("Cannot cancel completed or already cancelled bookings.")
        self.status = BookingStatus.CANCELLED

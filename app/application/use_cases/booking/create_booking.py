import uuid
from datetime import datetime
from app.domain.entities.booking import Booking
from app.domain.repositories.booking_repo import BookingRepository
from app.domain.repositories.vehicle_repo import VehicleRepository

class CreateBookingUseCase:
    def __init__(self, booking_repo: BookingRepository, vehicle_repo: VehicleRepository):
        self.booking_repo = booking_repo
        self.vehicle_repo = vehicle_repo

    async def execute(self, customer_id: uuid.UUID, vehicle_id: uuid.UUID, 
                      start_time: datetime, end_time: datetime) -> Booking:
        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")
        
        # Check vehicle existence
        vehicle = await self.vehicle_repo.get_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found.")
            
        # Check schedule conflicts
        is_available = await self.booking_repo.check_availability(vehicle_id, start_time, end_time)
        if not is_available:
            raise ValueError("Vehicle is already booked for the selected time range.")

        # Calculate fare
        duration = end_time - start_time
        hours = max(1.0, duration.total_seconds() / 3600.0)
        total_fare = round(hours * vehicle.price_per_hour, 2)

        # Create booking
        booking = Booking(
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            start_time=start_time,
            end_time=end_time,
            total_fare=total_fare
        )

        # Save booking and update vehicle status
        await self.booking_repo.save(booking)
        
        # Optionally update vehicle status (for simple catalog flags)
        # Note: In a fully calendar-based system, availability depends on datetime ranges, 
        # but setting a general status helps filter simple "right now" queries.
        vehicle.book()
        await self.vehicle_repo.save(vehicle)

        return booking

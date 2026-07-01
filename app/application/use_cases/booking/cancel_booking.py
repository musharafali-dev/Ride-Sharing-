import uuid
from app.domain.entities.booking import Booking, BookingStatus
from app.domain.repositories.booking_repo import BookingRepository
from app.domain.repositories.vehicle_repo import VehicleRepository

class CancelBookingUseCase:
    def __init__(self, booking_repo: BookingRepository, vehicle_repo: VehicleRepository):
        self.booking_repo = booking_repo
        self.vehicle_repo = vehicle_repo

    async def execute(self, booking_id: uuid.UUID) -> Booking:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if booking.status == BookingStatus.CANCELLED:
            return booking

        # Cancel the booking
        booking.cancel()
        await self.booking_repo.save(booking)

        # Release the vehicle
        vehicle = await self.vehicle_repo.get_by_id(booking.vehicle_id)
        if vehicle:
            vehicle.release()
            await self.vehicle_repo.save(vehicle)

        return booking

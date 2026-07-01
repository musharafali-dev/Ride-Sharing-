import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.booking import Booking, BookingStatus
from app.domain.repositories.booking_repo import BookingRepository
from app.infrastructure.database.models.booking_model import BookingModel

class SQLBookingRepository(BookingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, booking_id: uuid.UUID) -> Optional[Booking]:
        result = await self.session.execute(
            select(BookingModel).where(BookingModel.id == booking_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_customer_id(self, customer_id: uuid.UUID) -> List[Booking]:
        result = await self.session.execute(
            select(BookingModel)
            .where(BookingModel.customer_id == customer_id)
            .order_by(BookingModel.created_at.desc())
        )
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def save(self, booking: Booking) -> None:
        result = await self.session.execute(
            select(BookingModel).where(BookingModel.id == booking.id)
        )
        model = result.scalar_one_or_none()

        if not model:
            model = BookingModel(
                id=booking.id,
                customer_id=booking.customer_id,
                vehicle_id=booking.vehicle_id,
                start_time=booking.start_time,
                end_time=booking.end_time,
                total_fare=booking.total_fare,
                status=booking.status,
                created_at=booking.created_at
            )
            self.session.add(model)
        else:
            model.status = booking.status
            model.start_time = booking.start_time
            model.end_time = booking.end_time
            model.total_fare = booking.total_fare

    async def check_availability(self, vehicle_id: uuid.UUID, start_time: datetime, end_time: datetime) -> bool:
        # Check overlapping bookings that are not cancelled
        result = await self.session.execute(
            select(BookingModel)
            .where(
                and_(
                    BookingModel.vehicle_id == vehicle_id,
                    BookingModel.status != BookingStatus.CANCELLED,
                    or_(
                        and_(BookingModel.start_time <= start_time, BookingModel.end_time > start_time),
                        and_(BookingModel.start_time < end_time, BookingModel.end_time >= end_time),
                        and_(BookingModel.start_time >= start_time, BookingModel.end_time <= end_time)
                    )
                )
            )
        )
        conflicting = result.scalars().all()
        return len(conflicting) == 0

    def _to_domain(self, model: BookingModel) -> Booking:
        return Booking(
            id=model.id,
            customer_id=model.customer_id,
            vehicle_id=model.vehicle_id,
            start_time=model.start_time,
            end_time=model.end_time,
            total_fare=model.total_fare,
            status=model.status,
            created_at=model.created_at
        )

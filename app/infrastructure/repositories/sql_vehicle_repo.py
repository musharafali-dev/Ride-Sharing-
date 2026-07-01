import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.vehicle import Vehicle, VehicleStatus
from app.domain.repositories.vehicle_repo import VehicleRepository
from app.infrastructure.database.models.user_model import VehicleModel

class SQLVehicleRepository(VehicleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, vehicle_id: uuid.UUID) -> Optional[Vehicle]:
        result = await self.session.execute(
            select(VehicleModel).where(VehicleModel.id == vehicle_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_all(self, category: Optional[str] = None) -> List[Vehicle]:
        stmt = select(VehicleModel)
        if category:
            stmt = stmt.where(VehicleModel.category == category)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def save(self, vehicle: Vehicle) -> None:
        result = await self.session.execute(
            select(VehicleModel).where(VehicleModel.id == vehicle.id)
        )
        model = result.scalar_one_or_none()

        if not model:
            model = VehicleModel(
                id=vehicle.id,
                category=vehicle.category,
                make=vehicle.make,
                model=vehicle.model,
                year=vehicle.year,
                color=vehicle.color,
                license_plate=vehicle.license_plate,
                price_per_hour=vehicle.price_per_hour,
                image_url=vehicle.image_url,
                status=vehicle.status
            )
            self.session.add(model)
        else:
            model.category = vehicle.category
            model.make = vehicle.make
            model.model = vehicle.model
            model.year = vehicle.year
            model.color = vehicle.color
            model.license_plate = vehicle.license_plate
            model.price_per_hour = vehicle.price_per_hour
            model.image_url = vehicle.image_url
            model.status = vehicle.status

    def _to_domain(self, model: VehicleModel) -> Vehicle:
        return Vehicle(
            id=model.id,
            category=model.category,
            make=model.make,
            model=model.model,
            year=model.year,
            color=model.color,
            license_plate=model.license_plate,
            price_per_hour=model.price_per_hour,
            image_url=model.image_url,
            status=model.status
        )

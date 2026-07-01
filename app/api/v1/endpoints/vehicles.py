from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import uuid
from app.api.v1.schemas.bookings import VehicleResponse
from app.api.deps import get_vehicle_repo
from app.infrastructure.repositories.sql_vehicle_repo import SQLVehicleRepository

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("", response_model=List[VehicleResponse])
async def list_vehicles(
    category: Optional[str] = None,
    vehicle_repo: SQLVehicleRepository = Depends(get_vehicle_repo)
):
    vehicles = await vehicle_repo.get_all(category=category)
    return [VehicleResponse.model_validate(v) for v in vehicles]

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: uuid.UUID,
    vehicle_repo: SQLVehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await vehicle_repo.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return VehicleResponse.model_validate(vehicle)

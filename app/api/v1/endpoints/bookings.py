from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid
from app.api.v1.schemas.bookings import CreateBookingRequest, BookingResponse, VehicleResponse
from app.api.deps import get_current_user, get_booking_repo, get_vehicle_repo
from app.domain.entities.user import User
from app.infrastructure.repositories.sql_booking_repo import SQLBookingRepository
from app.infrastructure.repositories.sql_vehicle_repo import SQLVehicleRepository
from app.application.use_cases.booking.create_booking import CreateBookingUseCase
from app.application.use_cases.booking.cancel_booking import CancelBookingUseCase

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    request: CreateBookingRequest,
    current_user: User = Depends(get_current_user),
    booking_repo: SQLBookingRepository = Depends(get_booking_repo),
    vehicle_repo: SQLVehicleRepository = Depends(get_vehicle_repo)
):
    use_case = CreateBookingUseCase(booking_repo, vehicle_repo)
    try:
        booking = await use_case.execute(
            customer_id=current_user.id,
            vehicle_id=request.vehicle_id,
            start_time=request.start_time,
            end_time=request.end_time
        )
        
        # Populate vehicle details for response
        vehicle = await vehicle_repo.get_by_id(booking.vehicle_id)
        response_data = BookingResponse.model_validate(booking)
        if vehicle:
            response_data.vehicle = VehicleResponse.model_validate(vehicle)
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me", response_model=List[BookingResponse])
async def list_my_bookings(
    current_user: User = Depends(get_current_user),
    booking_repo: SQLBookingRepository = Depends(get_booking_repo),
    vehicle_repo: SQLVehicleRepository = Depends(get_vehicle_repo)
):
    bookings = await booking_repo.get_by_customer_id(current_user.id)
    response_list = []
    for b in bookings:
        vehicle = await vehicle_repo.get_by_id(b.vehicle_id)
        res = BookingResponse.model_validate(b)
        if vehicle:
            res.vehicle = VehicleResponse.model_validate(vehicle)
        response_list.append(res)
    return response_list

@router.post("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    booking_repo: SQLBookingRepository = Depends(get_booking_repo),
    vehicle_repo: SQLVehicleRepository = Depends(get_vehicle_repo)
):
    # Verify booking belongs to current user
    booking = await booking_repo.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    use_case = CancelBookingUseCase(booking_repo, vehicle_repo)
    try:
        updated_booking = await use_case.execute(booking_id)
        vehicle = await vehicle_repo.get_by_id(updated_booking.vehicle_id)
        res = BookingResponse.model_validate(updated_booking)
        if vehicle:
            res.vehicle = VehicleResponse.model_validate(vehicle)
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

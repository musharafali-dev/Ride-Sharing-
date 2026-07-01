from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.booking import BookingCreate, BookingResponse
from app.models.booking import Booking
from app.models.vehicle import Vehicle
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Calculate price if vehicle is chosen
    if booking_in.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == booking_in.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        if not vehicle.is_available:
            raise HTTPException(status_code=400, detail="Vehicle is not available")
        
        # Simple calculate total amount based on duration
        duration = booking_in.end_time - booking_in.start_time
        hours = duration.total_seconds() / 3600.0
        days = max(1.0, duration.days)
        
        if booking_in.booking_type == "ride":
            total_amount = hours * vehicle.price_per_hour
        else: # rental
            total_amount = days * vehicle.price_per_day
    else:
        total_amount = booking_in.total_amount

    db_booking = Booking(
        customer_id=current_user.id,
        vehicle_id=booking_in.vehicle_id,
        driver_id=booking_in.driver_id,
        tour_id=booking_in.tour_id,
        booking_type=booking_in.booking_type,
        status="pending",
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
        total_amount=total_amount
    )
    
    # Mark vehicle as booked if rental
    if booking_in.vehicle_id and booking_in.booking_type == "rental":
        vehicle = db.query(Vehicle).filter(Vehicle.id == booking_in.vehicle_id).first()
        if vehicle:
            vehicle.is_available = False

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=List[BookingResponse])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Booking).all()
    elif current_user.role == "driver":
        return db.query(Booking).filter(Booking.driver_id == current_user.id).all()
    elif current_user.role == "owner":
        # Find bookings on vehicles owned by this user
        return db.query(Booking).join(Vehicle).filter(Vehicle.owner_id == current_user.id).all()
    else: # customer
        return db.query(Booking).filter(Booking.customer_id == current_user.id).all()

@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(
    booking_id: str,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    booking.status = status
    
    # Release vehicle if booking is completed or cancelled
    if status in ["completed", "cancelled"] and booking.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == booking.vehicle_id).first()
        if vehicle:
            vehicle.is_available = True
            
    db.commit()
    db.refresh(booking)
    return booking

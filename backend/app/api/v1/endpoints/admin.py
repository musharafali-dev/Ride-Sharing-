from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.booking import Booking
from app.models.payment import Payment

router = APIRouter()

@router.get("/dashboard/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    total_users = db.query(User).count()
    total_vehicles = db.query(Vehicle).count()
    total_bookings = db.query(Booking).count()
    
    payments = db.query(Payment).filter(Payment.status == "completed").all()
    total_revenue = sum(p.amount for p in payments)
    
    return {
        "users_count": total_users,
        "vehicles_count": total_vehicles,
        "bookings_count": total_bookings,
        "total_revenue": total_revenue
    }

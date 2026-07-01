from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.v1.schemas.users import UserResponse
from app.api.deps import get_current_user, get_user_repo
from app.domain.entities.user import User, UserRole
from app.infrastructure.repositories.sql_user_repo import SQLUserRepository
from sqlalchemy import select
from app.infrastructure.database.models.user_model import UserModel

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operation restricted to administrators only"
        )
    return current_user

@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
async def list_users(user_repo: SQLUserRepository = Depends(get_user_repo)):
    # Retrieve all users directly from session
    result = await user_repo.session.execute(select(UserModel).order_by(UserModel.created_at.desc()))
    models = result.scalars().all()
    return [user_repo._to_domain(m) for m in models]

@router.get("/analytics/overview", dependencies=[Depends(require_admin)])
async def get_analytics_overview(
    user_repo: SQLUserRepository = Depends(get_user_repo)
):
    # Quick count query simulation
    from sqlalchemy import func
    from app.infrastructure.database.models.user_model import VehicleModel
    from app.infrastructure.database.models.booking_model import BookingModel
    
    users_count = (await user_repo.session.execute(select(func.count(UserModel.id)))).scalar() or 0
    vehicles_count = (await user_repo.session.execute(select(func.count(VehicleModel.id)))).scalar() or 0
    bookings_count = (await user_repo.session.execute(select(func.count(BookingModel.id)))).scalar() or 0
    
    return {
        "total_registered_users": users_count,
        "total_vehicles_in_fleet": vehicles_count,
        "total_bookings_processed": bookings_count,
        "system_status": "healthy"
    }

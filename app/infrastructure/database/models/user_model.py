import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
from app.domain.entities.user import UserRole
from app.domain.entities.vehicle import VehicleStatus

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name="user_role"), default=UserRole.RIDER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    bookings = relationship("BookingModel", back_populates="customer", cascade="all, delete-orphan")
    payments = relationship("PaymentModel", back_populates="user")


class VehicleModel(Base):
    __tablename__ = "vehicles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="car") # car, van, bike, coaster
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    price_per_hour: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[VehicleStatus] = mapped_column(SAEnum(VehicleStatus, name="vehicle_status"), default=VehicleStatus.AVAILABLE, nullable=False)

    # Relationships
    bookings = relationship("BookingModel", back_populates="vehicle", cascade="all, delete-orphan")

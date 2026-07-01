import uuid
from datetime import datetime

from app.db.session import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    category = Column(
        String, nullable=False
    )  # city_ride, car_rental, bike_rental, bus_coaster, luxury
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    price_per_day = Column(Float, nullable=False, default=0.0)
    price_per_hour = Column(Float, nullable=False, default=0.0)
    seats = Column(Integer, nullable=False, default=4)
    transmission = Column(String, default="automatic")  # manual, automatic
    fuel_type = Column(String, default="petrol")  # petrol, diesel, electric, hybrid
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="vehicles")
    bookings = relationship("Booking", back_populates="vehicle")

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(String, ForeignKey("users.id"), nullable=True)
    tour_id = Column(String, ForeignKey("tours.id"), nullable=True)
    booking_type = Column(String, nullable=False) # ride, rental, tour
    status = Column(String, default="pending") # pending, active, completed, cancelled
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("User", back_populates="bookings", foreign_keys=[customer_id])
    driver = relationship("User", back_populates="trips", foreign_keys=[driver_id])
    vehicle = relationship("Vehicle", back_populates="bookings")
    tour = relationship("Tour", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")
    reviews = relationship("Review", back_populates="booking")

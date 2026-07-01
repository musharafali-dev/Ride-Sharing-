import uuid
from datetime import datetime

from app.db.session import Base
from sqlalchemy import Column, DateTime, String


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_id = Column(String, nullable=True)  # Scope messaging to a booking if needed
    sender_id = Column(String, nullable=False)
    receiver_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

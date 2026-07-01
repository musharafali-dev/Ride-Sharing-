import uuid
from datetime import datetime

from app.db.session import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, String


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(
        String, nullable=False
    )  # credit (add funds), debit (payment)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

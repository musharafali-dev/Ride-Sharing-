import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.user import User
from app.models.wallet import WalletTransaction

router = APIRouter()

@router.post("/", response_model=PaymentResponse)
def process_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == payment_in.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    if payment_in.payment_method == "wallet":
        if current_user.wallet_balance < payment_in.amount:
            raise HTTPException(status_code=400, detail="Insufficient wallet balance")
            
        current_user.wallet_balance -= payment_in.amount
        
        # Log wallet debit
        db_tx = WalletTransaction(
            user_id=current_user.id,
            amount=payment_in.amount,
            transaction_type="debit",
            description=f"Paid for booking {booking.id}"
        )
        db.add(db_tx)
        
    # Generate mock transaction reference
    tx_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    db_payment = Payment(
        booking_id=payment_in.booking_id,
        amount=payment_in.amount,
        payment_method=payment_in.payment_method,
        status="completed",
        transaction_id=tx_id
    )
    
    booking.status = "active"
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

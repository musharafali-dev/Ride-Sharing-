from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.wallet import WalletTransactionResponse, WalletAddFunds
from app.models.wallet import WalletTransaction
from app.models.user import User

router = APIRouter()

@router.get("/transactions", response_model=List[WalletTransactionResponse])
def get_wallet_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WalletTransaction).filter(WalletTransaction.user_id == current_user.id).all()

@router.post("/add-funds", response_model=WalletTransactionResponse)
def add_funds(
    wallet_in: WalletAddFunds,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if wallet_in.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Update user balance
    current_user.wallet_balance += wallet_in.amount
    
    # Create transaction
    db_tx = WalletTransaction(
        user_id=current_user.id,
        amount=wallet_in.amount,
        transaction_type="credit",
        description=f"Funded wallet via {wallet_in.payment_method}"
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

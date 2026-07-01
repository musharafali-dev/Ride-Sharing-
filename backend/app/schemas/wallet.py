from pydantic import BaseModel
from datetime import datetime

class WalletTransactionBase(BaseModel):
    amount: float
    transaction_type: str # credit, debit
    description: str

class WalletTransactionCreate(WalletTransactionBase):
    pass

class WalletTransactionResponse(WalletTransactionBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class WalletAddFunds(BaseModel):
    amount: float
    payment_method: str # card, jazzcash, easypaisa

from typing import List
from pydantic import BaseModel
from typing_extensions import Optional

from app.schemas.purchase import PurchaseHistory
from app.schemas.transaction import TransactionHistory


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class InfoResponse(BaseModel):
    coins: int
    inventory: Optional[List[PurchaseHistory]] = []
    coinHistory: Optional[TransactionHistory] = []

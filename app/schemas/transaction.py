from typing import List, Optional

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    toUser: str
    amount: int = Field(..., gt=0)


class TransactionCreate(BaseModel):
    sender_id: int
    recipient_id: int
    amount: int = Field(..., gt=0)


class TransactionReceivedHistory(BaseModel):
    fromUser: str
    amount: int = Field(..., gt=0)


class TransactionSentHistory(BaseModel):
    toUser: str
    amount: int = Field(..., gt=0)


class TransactionHistory(BaseModel):
    received: Optional[List[TransactionReceivedHistory]] = []
    sent: Optional[List[TransactionSentHistory]] = []

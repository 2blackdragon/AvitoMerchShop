from pydantic import BaseModel, Field


class PurchaseCreate(BaseModel):
    merch_id: int
    user_id: int
    quantity: int = Field(..., gt=0)


class PurchaseHistory(BaseModel):
    name: str
    quantity: int
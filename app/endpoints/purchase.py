from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.cruds.merch import get_merch
from app.cruds.purchase import create_purchase
from app.cruds.user import reduce_coins
from app.db.database import get_db
from app.models.user import User
from app.schemas.purchase import PurchaseCreate
from app.services.user import get_current_user


router = APIRouter()

@router.post("/buy/{item}")
async def buy_merch(item: str, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    merch = get_merch(db, item)
    if not merch:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found.")

    if quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be positive.")

    if current_user.coins_balance < merch.price * quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough coins.")

    reduce_coins(db, current_user, merch.price * quantity)

    purchase = create_purchase(db, PurchaseCreate(merch_id=merch.id,
                                       user_id=current_user.id,
                                       quantity=quantity))

    return purchase



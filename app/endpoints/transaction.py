from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.transaction import TransactionRequest, TransactionCreate
from app.services.user import get_current_user
from app.cruds.user import get_user, add_coins, reduce_coins
from app.cruds.transaction import create_transaction

router = APIRouter()


@router.post("/sendCoin")
async def send_coin(request: TransactionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(request)
    sender = get_user(db, current_user.username)
    if sender.coins_balance < request.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough coins.")

    recipient = get_user(db, username=request.toUser)
    if not recipient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recipient not found.")

    if sender.id == recipient.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot send coins to yourself.")

    reduce_coins(db, sender, request.amount)
    add_coins(db, recipient, request.amount)


    transaction = create_transaction(db, TransactionCreate(sender_id=sender.id,
                                                           recipient_id=recipient.id,
                                                           amount=request.amount))

    return transaction

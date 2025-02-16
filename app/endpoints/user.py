from statistics import quantiles

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import from_

from app.cruds.purchase import get_user_purchases
from app.cruds.transaction import get_received_transactions, get_sent_transactions
from app.db.database import get_db
from app.models.user import User
from app.schemas.purchase import PurchaseHistory
from app.schemas.transaction import TransactionReceivedHistory, TransactionSentHistory, TransactionHistory
from app.schemas.user import InfoResponse
from app.services.user import create_access_token, authenticate_user, get_current_user

router = APIRouter()


@router.post("/auth")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/info")
async def user_info(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    coins = user.coins_balance

    received_transactions = [
        TransactionReceivedHistory(fromUser=t.fromUser, amount=t.amount)
        for t in get_received_transactions(db, user.id)
    ]

    sent_transactions = [
        TransactionSentHistory(toUser=t.toUser, amount=t.amount)
        for t in get_sent_transactions(db, user.id)
    ]


    purchases = [
        PurchaseHistory(name=t.name, quantity=t.total_quantity)
        for t in get_user_purchases(db, user.id)
    ]

    info_data = InfoResponse(coins=coins,
                             inventory=purchases,
                             coinHistory=TransactionHistory(received=received_transactions,
                                                            sent=sent_transactions))


    return info_data

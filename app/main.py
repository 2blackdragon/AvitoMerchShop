from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.endpoints.user import router as user_router
from app.endpoints.transaction import router as transaction_router
from app.endpoints.purchase import router as purchase_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
app.include_router(purchase_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()

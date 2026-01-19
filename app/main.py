from fastapi import FastAPI, Depends, Header, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.sql import text
from typing import Annotated
import uuid

from app.database import get_db, engine
from app.models import Transaction, TransactionStatusDict, TransactionTypeDict
from app.schemas import TransactionRequest, SessionResponse, TpayDBResponse

# --- App Setup ---
app = FastAPI(
    title="TRUSTED-PAY API Reference",
    version="0.1",
    servers=[{"url": "http://localhost:8000"}, {"url": "https://trusted-pay.io"}],
    docs_url="/swagger",
    redoc_url="/redoc"
)

# --- Telemetry ---
Instrumentator().instrument(app).expose(app)

# --- Auth Dependency (FIXED) ---
async def verify_token(
    # usage of alias="Authorization" ensures it matches your Spec and curl expectations
    authorization: Annotated[str, Header(alias="Authorization", description="Bearer <token>")]
):
    """
    Validates presence of the Authorization header.
    In Swagger UI, you must type 'Bearer <your-token>' into the field.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    return authorization

# --- Health Probes ---
@app.get("/health/live", tags=["Health"])
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready", tags=["Health"])
async def readiness():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

# --- Routes matching OpenAPI paths ---

@app.post("/tpay/backend/transaction", 
          response_model=SessionResponse, 
          tags=["tpay"], 
          operation_id="createTransaction")
async def create_transaction(
    tx_request: TransactionRequest, 
    auth: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    # Map request to DB model
    new_tx = Transaction(
        amount=tx_request.amount,
        currency=tx_request.currency,
        purpose=tx_request.purpose,
        recipient=tx_request.recipient,
        recipient_iban=tx_request.recipientIban,
        recipient_bic=tx_request.recipientBic,
        sender_iban=tx_request.senderIban,
        callback_url=tx_request.callbackUrl,
        transaction_type=tx_request.transactionType,
        transaction_status="CREATED", # Default status
        end_user_access_token=tx_request.endUserAccessToken
    )
    
    db.add(new_tx)
    await db.commit()
    await db.refresh(new_tx)
    
    # Generate a dummy session ID (logic not specified in spec, assumed generated here)
    session_id = str(uuid.uuid4())
    
    return SessionResponse(sessionId=session_id, transactionId=new_tx.id)


@app.get("/tpay/backend/transaction/{transactionId}", 
         response_model=TpayDBResponse, 
         tags=["tpay"], 
         operation_id="getTransaction")
async def get_transaction(
    transactionId: str, 
    auth: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    query = select(Transaction).where(Transaction.id == transactionId)
    result = await db.execute(query)
    tx = result.scalars().first()
    
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    # Manual mapping to CamelCase response if needed, or Pydantic handles snake_case -> camelCase mapping
    return TpayDBResponse(
        id=tx.id,
        dateCreated=tx.date_created,
        dateModified=tx.date_modified,
        tenant=tx.tenant,
        transactionType=tx.transaction_type,
        transactionStatus=tx.transaction_status,
        recipient=tx.recipient,
        recipientIban=tx.recipient_iban,
        recipientBic=tx.recipient_bic,
        senderIban=tx.sender_iban,
        amount=tx.amount,
        currency=tx.currency,
        purpose=tx.purpose,
        callbackUrl=tx.callback_url
    )

@app.post("/tpay/backend/token", 
          tags=["tpay"], 
          operation_id="createToken")
async def create_token(auth: str = Depends(verify_token)):
    """Simple token generation stub matching the UUID response format"""
    return str(uuid.uuid4())
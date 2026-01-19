from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime
from enum import Enum

# --- Enums from Spec ---
class TransactionTypeEnum(str, Enum):
    PAYMENT = "PAYMENT"
    VERIFICATION = "VERIFICATION"

class TransactionStatusEnum(str, Enum):
    CREATED = "CREATED"
    PROVIDER_SELECTED = "PROVIDER_SELECTED"
    TRANSFER_STARTED = "TRANSFER_STARTED"
    BANK_ACCESS_CONSENT = "BANK_ACCESS_CONSENT"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

# --- Request Models ---
class TransactionRequest(BaseModel):
    """Matches 'Transaction' schema in OpenAPI"""
    amount: str = Field(..., pattern=r"^[0-9]{1,5}\.[0-9]{2}$")
    currency: str = Field(..., pattern=r"^[A-Z]{3}$")
    purpose: str = Field(..., min_length=1, max_length=140, pattern=r"^[a-zA-Z0-9/\-\?:\(\)\.\,\'\+ ]*$")
    recipient: str = Field(..., min_length=1, max_length=70, pattern=r"^[a-zA-Z0-9/\-\?:\(\)\.\,\'\+ ]*$")
    callbackUrl: str = Field(..., alias="callbackUrl")
    
    # Optional fields
    transactionType: Optional[TransactionTypeEnum] = None
    recipientIban: Optional[str] = Field(None, pattern=r"^[A-Z]{2}[0-9]{2}[0-9A-Z]{1,30}$")
    recipientBic: Optional[str] = Field(None, pattern=r"^[A-Z]{4}[A-Z]{2}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3})?$")
    senderIban: Optional[str] = Field(None, pattern=r"^[A-Z]{2}[0-9]{2}[0-9A-Z]{1,30}$")
    endUserAccessToken: Optional[str] = Field(None, pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    class Config:
        populate_by_name = True

# --- Response Models ---
class SessionResponse(BaseModel):
    """Matches 'Session' schema"""
    sessionId: str
    transactionId: str

class TpayDBResponse(BaseModel):
    """Matches 'tpayDB' schema"""
    id: str
    dateCreated: datetime
    dateModified: Optional[datetime] = None
    tenant: Optional[str] = None
    transactionType: Optional[TransactionTypeEnum] = None
    transactionStatus: TransactionStatusEnum
    provider: Optional[str] = None
    sender: Optional[str] = None
    senderIban: Optional[str] = None
    senderBic: Optional[str] = None
    recipient: Optional[str] = None
    recipientIban: Optional[str] = None
    recipientBic: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    purpose: Optional[str] = None
    callbackUrl: Optional[str] = None

    class Config:
        from_attributes = True # updated for Pydantic v2
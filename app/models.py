import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# --- Dictionaries (Reference Data) ---
class TransactionTypeDict(Base):
    """Dictionary for allowed transaction types (PAYMENT, VERIFICATION)"""
    __tablename__ = "dict_transaction_types"
    code = Column(String, primary_key=True)  # e.g., "PAYMENT"
    description = Column(String, nullable=True)

class TransactionStatusDict(Base):
    """Dictionary for allowed statuses (CREATED, SUCCESS, etc.)"""
    __tablename__ = "dict_transaction_statuses"
    code = Column(String, primary_key=True)  # e.g., "CREATED"
    description = Column(String, nullable=True)

# --- Main Transaction Table ---
class Transaction(Base):
    __tablename__ = "transactions"

    # ID matches 'tpayDB' schema
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # Timestamps
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    # Core Data
    tenant = Column(String, nullable=True) # Optional in your spec, but good for multi-tenancy
    amount = Column(String, nullable=False) # Stored as string to preserve precision per spec regex
    currency = Column(String(3), nullable=False)
    purpose = Column(String(140), nullable=False)
    callback_url = Column(String, nullable=False)
    
    # Relations to Dictionaries
    transaction_type = Column(String, ForeignKey("dict_transaction_types.code"))
    transaction_status = Column(String, ForeignKey("dict_transaction_statuses.code"), default="CREATED")

    # Participants
    sender = Column(String, nullable=True)
    sender_iban = Column(String, nullable=True)
    sender_bic = Column(String, nullable=True)
    
    recipient = Column(String, nullable=False)
    recipient_iban = Column(String, nullable=True)
    recipient_bic = Column(String, nullable=True)
    
    provider_id = Column(String, nullable=True) # UUID of provider
    end_user_access_token = Column(String, nullable=True)
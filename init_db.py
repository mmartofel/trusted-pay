import asyncio
from app.database import engine
from app.models import Base, TransactionTypeDict, TransactionStatusDict  # <--- FIXED IMPORT
from sqlalchemy.ext.asyncio import AsyncSession

async def init_dictionaries():
    # 1. Create tables
    async with engine.begin() as conn:
        # This creates all tables defined in models.py (transactions, dictionaries)
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tables created successfully.")

    # 2. Populate Dictionary Data
    async with AsyncSession(engine) as session:
        # Transaction Types
        types = [
            TransactionTypeDict(code="PAYMENT", description="Standard Payment"),
            TransactionTypeDict(code="VERIFICATION", description="Account Verification")
        ]
        
        # Transaction Statuses
        statuses = [
            TransactionStatusDict(code="CREATED", description="Transaction Created"),
            TransactionStatusDict(code="PROVIDER_SELECTED", description="Provider Selected"),
            TransactionStatusDict(code="TRANSFER_STARTED", description="Transfer Started"),
            TransactionStatusDict(code="BANK_ACCESS_CONSENT", description="Bank Consent Given"),
            TransactionStatusDict(code="SUCCESS", description="Transaction Successful"),
            TransactionStatusDict(code="ERROR", description="Transaction Failed"),
        ]
        
        # Merge ensures we don't get duplicate key errors if we run this twice
        for item in types + statuses:
            await session.merge(item)
        
        await session.commit()
    
    print("✅ Dictionaries populated successfully.")

if __name__ == "__main__":
    asyncio.run(init_dictionaries())    
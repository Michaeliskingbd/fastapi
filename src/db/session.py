from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
#Creates the database engine
#Uses your .env connection string
#echo=True → logs SQL queries (useful for debugging)

SessionLocal = async_sessionmaker(
    #Creates a session factory
    bind=engine,
    #Connects session to your database engine
    class_=AsyncSession,
    #Specifies async session type
    expire_on_commit=False
    #Prevents objects from becoming unusable after commit
    #Keeps data accessible without reloading
)
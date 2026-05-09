from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import text, SQLModel
from src.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
      #  statement = text("SELECT 'hello';")
      #  result = await conn.execute(statement)
      #  print(result.all())
      from src.Student.models import Student
      await conn.run_sync(SQLModel.metadata.create_all)
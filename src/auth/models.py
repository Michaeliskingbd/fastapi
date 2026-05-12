from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,nullable=False, default=uuid.uuid4)
    )

    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    is_active: bool = Field(default=True)
    is_verifled: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
  
    def __repr__(self):
        return f"<User {self.username}>"
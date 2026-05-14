from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,nullable=False, default=uuid.uuid4)
    )

    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str = Field(exclude=True)
    full_name: str
    is_active: bool = Field(default=True)
    is_verifled: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


    
def __repr__(self):
        return f"<User {self.username}>"






class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id", index=True
    )

    token_hash: str = Field(index=True, unique=True)

    expires_at: datetime

    is_revoked: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    replaced_by: str | None = Field(default=None)

    __table_args__ = (
        Index("ix_refresh_user_active", "user_id", "is_revoked"),
    )
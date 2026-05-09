from sqlmodel import SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class Student(SQLModel, table=True) :
    __tablename__ = "Students"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4

        )
    )
    name: str
    course: str
    age: int
    gender: str
    location: str
    phone: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Student {self.name}>"
    


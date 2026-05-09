from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.Student.models import Student
import uuid


# CREATE
async def create_student(session: AsyncSession, student_data: Student):
    session.add(student_data)
    await session.commit()
    await session.refresh(student_data)
    return student_data


# GET ALL
async def get_students(session: AsyncSession):
    result = await session.execute(select(Student))
    return result.scalars().all()


# GET ONE
async def get_student(session: AsyncSession, student_id: uuid.UUID):
    result = await session.execute(
        select(Student).where(Student.uid == student_id)
    )
    return result.scalar_one_or_none()


# UPDATE
async def update_student(session: AsyncSession, student_id: uuid.UUID, data: dict):
    student = await get_student(session, student_id)

    if not student:
        return None

    for key, value in data.items():
        setattr(student, key, value)

    await session.commit()
    await session.refresh(student)
    return student


# DELETE
async def delete_student(session: AsyncSession, student_id: uuid.UUID):
    student = await get_student(session, student_id)

    if not student:
        return None

    await session.delete(student)
    await session.commit()
    return student
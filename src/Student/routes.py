from fastapi import FastAPI, HTTPException
from .data import students
from .schema import Student
from src.Student.service import create_student

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import SessionLocal

from fastapi import APIRouter
router = APIRouter()



async def get_session():
    async with SessionLocal() as session:
        yield session


# @router.get("/")
# async def pilot_endpoint():
 #   return {"message": "Hello mike"} 


@router.get("/")
async def get_students():
    return students

# Create 
@router.post("/")
async def create(student: Student, session: AsyncSession = Depends(get_session)):
    return await create_student(session, student)
"""
@router.post("/create")
async def create_student(student:Student):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "course": student.course
    }
    
    students.append(new_student)

    return {
        "message": "student created successfully",
        "data" : students
    }

@router.get("/{student_id}")
async def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="student not found")
        

@router.put("/{student_id}")
async def update_student(student_id: int, updated_student: Student):

    for student in students:
        if student["id"] == student_id:

            student["name"] = updated_student.name
            student["age"] = updated_student.age

            return {
                "message": "student updated",
                "data": student
            }

    raise HTTPException(status_code=404, detail="student not found")



@router.delete("/{student_id}")
async def delete_student(student_id: int):

    for student in students:
        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "student deleted"
            }

    raise HTTPException(status_code=404, detail="student not found")    
    """
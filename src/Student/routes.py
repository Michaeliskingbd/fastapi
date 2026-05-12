from .schema import StudentCreate
from src.Student.models import Student
from src.Student.service import create_student,get_students,get_student,update_student,delete_student
from fastapi import Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import SessionLocal
from fastapi import APIRouter
router = APIRouter()
import uuid



async def get_session():
    #Defines a function that will provide a DB session
    async with SessionLocal() as session:
        #Creates a new session per request
        #SessionLocal comes from your session config
        yield session
        #Sends the session to FastAPI
        #FastAPI injects it into your route
        #After request finishes → session is closed automatically

# Create 
@router.post("/create")
#Defines a POST endpoint
#URL: /create (combined with your prefix)
async def create(
    student: StudentCreate,
    #Request body
    #Validated using your Pydantic schema
    #Ensures correct data format
    session: AsyncSession = Depends(get_session)
    #FastAPI injects a DB session here
    #Depends(get_session) calls the function above
):
    db_student = Student(**student.model_dump()) 
    #Converts schema → database model
    #model_dump() turns schema into dict
    #Student(...) creates a real DB object
    return await create_student(session, db_student)
    #Calls service function
    #Passes:
    #session
    #model object
    #Returns saved data

#Get All
@router.get("/")
#→ Handles GET requests to /students/
async def get_all( session:AsyncSession = Depends(get_session)):
    #→ Injects a database session per request
    return await get_students(session)
#→ Calls your service function to fetch all records

#Get Single
@router.get("/{student_id}")
async def get_single(student_id: uuid.UUID, session:AsyncSession = Depends(get_session)): #→ Automatically validates UUID format
    student =  await get_student(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

#Update
from fastapi import HTTPException
import uuid

@router.put("/{student_id}")
async def update(
    student_id: uuid.UUID,
    data: StudentCreate,  # or StudentUpdate if you create one later
    session: AsyncSession = Depends(get_session)
):
    updated_student = await update_student(
        session,
        student_id,
        data.model_dump()
    )

    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student

#Delete
@router.delete("/{student_id}")
async def delete(
    student_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    deleted_student = await delete_student(session, student_id)

    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}

#Merging route + services
""""
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.session import SessionLocal
from src.Student.schema import StudentCreate
from src.Student.models import Student

router = APIRouter()


# session dependency
async def get_session():
    async with SessionLocal() as session:
        yield session


# CREATE (merged)
@router.post("/create")
async def create(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    # convert schema → model
    db_student = Student(**student.model_dump())

    # DB operations (previously in service)
    session.add(db_student)
    await session.commit()
    await session.refresh(db_student)

    return db_student
"""
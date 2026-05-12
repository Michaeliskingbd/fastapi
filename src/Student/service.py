from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.Student.models import Student
import uuid


# CREATE
async def create_student(session: AsyncSession, student_data: Student): #session → database session (used to talk to DB)  
    #student_data → instance of your Student model (table)
    session.add(student_data)
    #Tells the ORM:
    #“Prepare this object to be inserted into the database”
    #Nothing is written yet (just staged)
    await session.commit()
    #Actually writes the data to PostgreSQL
    #Without this, nothing is saved
    await session.refresh(student_data)
    #Reloads the object from the DB
    #Important because:
    #UUID gets generated
    #timestamps get filled
    #Now student_data contains real DB values
    return student_data
    #Returns the saved object back to the route


# GET ALL
async def get_students(session: AsyncSession):
    #Defines an async function
    #Accepts a database session (AsyncSession)
    #This session is used to talk to PostgreSQL
    result = await session.execute(select(Student))
    #Sends a SQL query to the database
    #select(Student) means:
    #“SELECT * FROM students”
    #await → waits for DB response (non-blocking)
    return result.scalars().all()
    #scalars() → extracts ORM objects (not raw rows)
    #all() → returns a Python list of Student objects


# GET ONE
async def get_student(session: AsyncSession, student_id: uuid.UUID):
    #Function takes:
    #DB session
    #student UUID
    result = await session.execute(
        select(Student).where(Student.uid == student_id)
    )
    #SQL query:
    #“SELECT * FROM students WHERE uid = ?”
    #Filters by primary key (uid)
    return result.scalar_one_or_none()
    #Returns:
    #single Student object if found
    #None if not found
    #Prevents errors if record doesn’t exist


# UPDATE
async def update_student(session: AsyncSession, student_id: uuid.UUID, data: dict):
        #Takes:
        #Session
        #student ID
        #update data (dictionary)
    student = await get_student(session, student_id)
    #Fetches student from DB first
    #Reuses your existing function

    if not student:
        return None
    #If student does not exist → stop function
    #Prevents updating non-existent record

    for key, value in data.items():
         #Loops through incoming fields
         #Example:
         #{"name": "Mike", "age": 25}
        setattr(student, key, value)
        #Dynamically updates model fields
        #Equivalent to:
        #student.name = "Mike"
        #student.age = 25

    await session.commit()
    #Saves changes to database
    await session.refresh(student)
    #Reloads updated data from DB
    #Ensures latest values are returned
    return student
    #Returns updated record


# DELETE
async def delete_student(session: AsyncSession, student_id: uuid.UUID):
    student = await get_student(session, student_id)

    if not student:
        return None

    await session.delete(student)
    await session.commit()
    return student
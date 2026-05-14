from fastapi import FastAPI
from src.Student.routes import router as student_router
from src.auth.routers import router as auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has been stopped")

API_VERSION = "v1"

app = FastAPI(
    title="Student_management_system",
    description="A practice REST API class",
    version=API_VERSION,
    lifespan=life_span
)

app.include_router(student_router,prefix=f"/api/{API_VERSION}/students",tags=["Students"])
                   
app.include_router(auth_router,prefix=f"/api/{API_VERSION}/auth",tags=["Auth"]               )




# postgresql://postgres:123456789@localhost:5432/fastapi_db




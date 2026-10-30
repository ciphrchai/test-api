import os
from pathlib import Path

from fastapi import FastAPI

from student_api.database import StudentRepository
from student_api.routers.students import router as students_router

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "students.db"


def create_app(database_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Student API",
        description="A simple backend API for managing students.",
        version="1.0.0",
    )
    configured_path = (
        database_path
        if database_path is not None
        else os.getenv("STUDENT_DB_PATH", str(DEFAULT_DATABASE_PATH))
    )
    app.state.student_repository = StudentRepository(configured_path)
    app.include_router(students_router)
    return app


app = create_app()

from fastapi import APIRouter, HTTPException, Request, Response, status

from student_api.database import StudentRepository
from student_api.schemas import StudentCreate, StudentRead

router = APIRouter(prefix="/students", tags=["students"])


def get_repository(request: Request) -> StudentRepository:
    return request.app.state.student_repository


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_student(student: StudentCreate, request: Request) -> StudentRead:
    return get_repository(request).create(student)


@router.get("", response_model=list[StudentRead])
def get_students(request: Request) -> list[StudentRead]:
    return get_repository(request).get_all()


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, request: Request) -> StudentRead:
    student = get_repository(request).get_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found.",
        )
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, request: Request) -> Response:
    if not get_repository(request).delete(student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# HTTP endpoints για τους μαθητες, πρεπει να ειναι οσο γινεται πιο λεπτο
"""
Student API routes.

Routes are responsible for:
- receiving HTTP requests
- validating input through schemas
- calling the service layer
- returning HTTP responses
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student.

    Args:
        student_in: Incoming validated student data.
        db: Database session provided by FastAPI dependency injection.

    Returns:
        The created student as API response data.
    """
    service = StudentService(db)
    return service.create_student(student_in)


@router.get("", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    """
    List all students.

    Args:
        db: Database session provided by FastAPI dependency injection.

    Returns:
        A list of students.
    """
    service = StudentService(db)
    return service.list_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single student by ID.

    Args:
        student_id: Student primary key.
        db: Database session provided by FastAPI dependency injection.

    Returns:
        The requested student.

    Raises:
        HTTPException: If the student does not exist.
    """
    service = StudentService(db)
    return service.get_student(student_id)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Delete a student by ID.

    Args:
        student_id: Student primary key.
        db: Database session provided by FastAPI dependency injection.

    Returns:
        Empty response with HTTP 204 status code.
    """
    service = StudentService(db)
    service.delete_student(student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# Κραταει το business logic, Βρισκεται αναμεσα σε routes και repositories
"""
Student service layer.

The service layer contains business logic and orchestration.

Why services are useful:
- routes stay thin and focused on HTTP concerns
- repositories stay focused on database concerns
- business rules live in one place
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate


class StudentService:
    """
    Service responsible for student-related business operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the service with a database session.

        Args:
            db: Active SQLAlchemy session.
        """
        self.repository = StudentRepository(db)

    def create_student(self, student_in: StudentCreate):
        """
        Create a new student.

        Args:
            student_in: Validated student creation input.

        Returns:
            The created student ORM object.
        """
        return self.repository.create(student_in)

    def list_students(self):
        """
        Return all students.

        Returns:
            A list of student ORM objects.
        """
        return self.repository.get_all()

    def get_student(self, student_id: int):
        """
        Retrieve a single student by ID.

        Args:
            student_id: Student primary key.

        Raises:
            HTTPException: If the student does not exist.

        Returns:
            The matching student ORM object.
        """
        student = self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )
        return student

    def delete_student(self, student_id: int) -> None:
        """
        Delete a student by ID.

        Args:
            student_id: Student primary key.

        Raises:
            HTTPException: If the student does not exist.
        """
        student = self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )
        self.repository.delete(student)

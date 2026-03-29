"""
Student service layer.

The service layer contains business logic and orchestration.

Why services are useful:
- routes stay thin and focused on HTTP concerns
- repositories stay focused on database concerns
- business rules live in one place
"""

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate


class StudentService:
    """
    Service responsible for student-related business operations.
    """

    def __init__(
        self,
        db: Session | None = None,
        repository: StudentRepository | None = None,
    ) -> None:
        """
        Initialize the service.

        The service can be initialized either with:
        - a database session, from which a repository will be created, or
        - a repository instance directly, which is useful in unit tests

        Args:
            db: Active SQLAlchemy session.
            repository: Optional repository instance.

        Raises:
            ValueError: If neither db nor repository is provided.
        """
        if repository is not None:
            self.repository = repository
        elif db is not None:
            self.repository = StudentRepository(db)
        else:
            raise ValueError("Either db or repository must be provided.")

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
            NotFoundError: If the student does not exist.

        Returns:
            The matching student ORM object.
        """
        student = self.repository.get_by_id(student_id)
        if student is None:
            raise NotFoundError("Student not found.")
        return student

    def delete_student(self, student_id: int) -> None:
        """
        Delete a student by ID.

        Args:
            student_id: Student primary key.

        Raises:
            NotFoundError: If the student does not exist.
        """
        student = self.repository.get_by_id(student_id)
        if student is None:
            raise NotFoundError("Student not found.")
        self.repository.delete(student)

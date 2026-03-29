# Το layer που μιλαει απευθειας με τη βαση(create, list all, get by id, delete)
"""
Student repository layer.

The repository is responsible for database access only.

Why repositories are useful:
- they isolate SQLAlchemy/database logic
- they keep services cleaner
- they make testing easier
- they reduce repeated query code
"""

from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


class StudentRepository:
    """
    Repository for student database operations.

    This class contains methods that directly interact with the database
    using a SQLAlchemy session.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db: Active SQLAlchemy session.
        """
        self.db = db

    def create(self, student_in: StudentCreate) -> Student:
        """
        Create and persist a new student in the database.

        Args:
            student_in: Validated input data for the new student.

        Returns:
            The newly created Student ORM object.
        """
        student = Student(
            first_name=student_in.first_name,
            last_name=student_in.last_name,
            center_name=student_in.center_name,
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_all(self) -> list[Student]:
        """
        Retrieve all students from the database.

        Returns:
            A list of Student ORM objects.
        """
        return self.db.query(Student).order_by(Student.id.asc()).all()

    def get_by_id(self, student_id: int) -> Student | None:
        """
        Retrieve a student by its unique identifier.

        Args:
            student_id: Student primary key.

        Returns:
            The Student ORM object if found, otherwise None.
        """
        return self.db.query(Student).filter(Student.id == student_id).first()

    def delete(self, student: Student) -> None:
        """
        Delete a student from the database.

        Args:
            student: The Student ORM object to delete.
        """
        self.db.delete(student)
        self.db.commit()

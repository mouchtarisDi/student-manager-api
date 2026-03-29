"""
Unit tests for the student service layer.

These tests validate business logic in isolation from FastAPI,
routing, and the real database.
"""

from unittest.mock import MagicMock

import pytest

from app.core.exceptions import NotFoundError
from app.schemas.student import StudentCreate
from app.services.student_service import StudentService


class DummyStudent:
    """
    Simple dummy student object used in service-layer unit tests.

    This avoids depending on a real SQLAlchemy ORM instance when the
    test only cares about service behavior.
    """

    def __init__(
        self,
        student_id: int,
        first_name: str,
        last_name: str,
        center_name: str,
    ) -> None:
        """
        Initialize a dummy student object.

        Args:
            student_id: Student identifier.
            first_name: Student first name.
            last_name: Student last name.
            center_name: Name of the center.
        """
        self.id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.center_name = center_name


@pytest.fixture
def mock_repository() -> MagicMock:
    """
    Create a mock student repository.

    Returns:
        A MagicMock object that simulates repository behavior.
    """
    return MagicMock()


@pytest.fixture
def student_service(mock_repository: MagicMock) -> StudentService:
    """
    Create a StudentService instance using a mocked repository.

    Args:
        mock_repository: Mocked repository fixture.

    Returns:
        A StudentService instance.
    """
    return StudentService(repository=mock_repository)


@pytest.fixture
def student_create_data() -> StudentCreate:
    """
    Create reusable valid student input data.

    Returns:
        A StudentCreate schema instance.
    """
    return StudentCreate(
        first_name="Dimitris",
        last_name="Mouchtaris",
        center_name="Giannitsa",
    )


def test_create_student_success(
    student_service: StudentService,
    mock_repository: MagicMock,
    student_create_data: StudentCreate,
) -> None:
    """
    Test that create_student delegates creation to the repository.
    """
    created_student = DummyStudent(
        student_id=1,
        first_name="Dimitris",
        last_name="Mouchtaris",
        center_name="Giannitsa",
    )

    mock_repository.create.return_value = created_student

    result = student_service.create_student(student_create_data)

    assert result.id == 1
    assert result.first_name == "Dimitris"
    assert result.last_name == "Mouchtaris"
    assert result.center_name == "Giannitsa"

    mock_repository.create.assert_called_once_with(student_create_data)


def test_list_students_returns_all_students(
    student_service: StudentService,
    mock_repository: MagicMock,
) -> None:
    """
    Test that list_students returns all students from the repository.
    """
    students = [
        DummyStudent(
            student_id=1,
            first_name="Dimitris",
            last_name="Mouchtaris",
            center_name="Giannitsa",
        ),
        DummyStudent(
            student_id=2,
            first_name="Maria",
            last_name="Papadopoulou",
            center_name="Krya Vrysi",
        ),
    ]

    mock_repository.get_all.return_value = students

    result = student_service.list_students()

    assert len(result) == 2
    assert result[0].first_name == "Dimitris"
    assert result[1].first_name == "Maria"

    mock_repository.get_all.assert_called_once()


def test_get_student_success(
    student_service: StudentService,
    mock_repository: MagicMock,
) -> None:
    """
    Test that get_student returns the requested student when it exists.
    """
    student = DummyStudent(
        student_id=1,
        first_name="Dimitris",
        last_name="Mouchtaris",
        center_name="Giannitsa",
    )

    mock_repository.get_by_id.return_value = student

    result = student_service.get_student(1)

    assert result.id == 1
    assert result.first_name == "Dimitris"
    assert result.last_name == "Mouchtaris"

    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_student_not_found_raises_error(
    student_service: StudentService,
    mock_repository: MagicMock,
) -> None:
    """
    Test that get_student raises NotFoundError when the student does not exist.
    """
    mock_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Student not found."):
        student_service.get_student(999)

    mock_repository.get_by_id.assert_called_once_with(999)


def test_delete_student_success(
    student_service: StudentService,
    mock_repository: MagicMock,
) -> None:
    """
    Test that delete_student removes the student when it exists.
    """
    student = DummyStudent(
        student_id=1,
        first_name="Dimitris",
        last_name="Mouchtaris",
        center_name="Giannitsa",
    )

    mock_repository.get_by_id.return_value = student

    student_service.delete_student(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(student)


def test_delete_student_not_found_raises_error(
    student_service: StudentService,
    mock_repository: MagicMock,
) -> None:
    """
    Test that delete_student raises NotFoundError when the student does not exist.
    """
    mock_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Student not found."):
        student_service.delete_student(123)

    mock_repository.get_by_id.assert_called_once_with(123)
    mock_repository.delete.assert_not_called()


def test_service_requires_db_or_repository() -> None:
    """
    Test that the service requires either a database session or a repository.
    """
    with pytest.raises(ValueError, match="Either db or repository must be provided."):
        StudentService()

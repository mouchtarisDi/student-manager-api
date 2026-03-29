# εδω οριζουμε τον πινακα students
"""
Student ORM model.

This module defines the database representation of a student.

A model describes:
- the table name
-the columns of the table
- the data types stored in the database

This is different from API schemas:
models are for the database,
schemas are for request/response validation
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Student(Base):
    """
    SQLAlchemy ORM model for the students table.

    Attributes:
        id: Primary key identifier of the student.
        first_name: The student's first name.
        last_name: The student's last name.
        center_name: Nmae of the center the student belongs to.
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    center_name: Mapped[str] = mapped_column(String(100), nullable=False)

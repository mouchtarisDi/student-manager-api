# Οριζουμετα schemas για το API, διαφορετικα για δημιουργια επιστροφη, λιστα κτλ
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    """
    Shared student fields used across multiple schemas.
    
    Attributes:
        first_name: Student's first name.
        last_name: Student's last name.
        center: Student's center.
    """

    #tτο ... σημαινει οτι το πεδιο ειναι υποχρεωτικο
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    center_name: str = Field(..., min_length=2, max_length=100)


class StudentCreate(StudentBase):
    """
    Schema used when creating a new student.

    This currently inherits all requires fields from StudentBase.
    It exists as a separate schema because creatin rules may deverge
    from other scheams later on (e.g. password confirmation, etc).
    """
    pass


class StudentResponse(StudentBase):
    """
    Schema used when returning a student to the API client.
    
    Attributes:
        id: Unique identifier of the student.
    """

    id: int 

    model_config = {"from_attributes": True}
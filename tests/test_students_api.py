"""
API tests for the student endpoints.

These tests verify that the student API behaves correctly from the outside,
through HTTP requests and responses.

What we test here:
- creating a student
- listing students
- retrieving a student by ID
- deleting a student
- handling non-existent students
"""


def test_create_student(client):
    """
    Test that a student can be created successfully.

    Steps:
    1. Send a POST request with valid student data.
    2. Confirm that the API returns HTTP 201.
    3. Confirm that the returned JSON contains the expected fields.
    """
    payload = {
        "first_name": "Dimitris",
        "last_name": "Mouchtaris",
        "center_name": "Giannitsa",
    }

    response = client.post("/students", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "Dimitris"
    assert data["last_name"] == "Mouchtaris"
    assert data["center_name"] == "Giannitsa"


def test_list_students(client):
    """
    Test that the students endpoint returns all created students.

    Steps:
    1. Create two students.
    2. Call GET /students.
    3. Confirm that both students are returned.
    """
    first_payload = {
        "first_name": "Dimitris",
        "last_name": "Mouchtaris",
        "center_name": "Giannitsa",
    }
    second_payload = {
        "first_name": "Maria",
        "last_name": "Papadopoulou",
        "center_name": "Krya Vrysi",
    }

    client.post("/students", json=first_payload)
    client.post("/students", json=second_payload)

    response = client.get("/students")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["first_name"] == "Dimitris"
    assert data[1]["first_name"] == "Maria"


def test_get_student_by_id(client):
    """
    Test that a single student can be retrieved by ID.

    Steps:
    1. Create a student.
    2. Request that student by ID.
    3. Confirm that the correct record is returned.
    """
    payload = {
        "first_name": "Dimitris",
        "last_name": "Mouchtaris",
        "center_name": "Giannitsa",
    }

    created_response = client.post("/students", json=payload)
    student_id = created_response.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == student_id
    assert data["first_name"] == "Dimitris"
    assert data["last_name"] == "Mouchtaris"
    assert data["center_name"] == "Giannitsa"


def test_get_student_by_id_not_found(client):
    """
    Test that requesting a non-existent student returns HTTP 404.
    """
    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found."


def test_delete_student(client):
    """
    Test that a student can be deleted successfully.

    Steps:
    1. Create a student.
    2. Delete that student.
    3. Confirm that the delete endpoint returns HTTP 204.
    4. Confirm that the student no longer exists.
    """
    payload = {
        "first_name": "Dimitris",
        "last_name": "Mouchtaris",
        "center_name": "Giannitsa",
    }

    created_response = client.post("/students", json=payload)
    student_id = created_response.json()["id"]

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 404


def test_delete_student_not_found(client):
    """
    Test that deleting a non-existent student returns HTTP 404.
    """
    response = client.delete("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found."

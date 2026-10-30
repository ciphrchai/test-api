from pathlib import Path

from fastapi.testclient import TestClient

from student_api.main import create_app


def make_client(tmp_path: Path) -> TestClient:
    app = create_app(tmp_path / "students.db")
    return TestClient(app)


def test_student_crud_flow(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        created_response = client.post(
            "/students",
            json={"name": "  Alex Morgan  ", "age": 20, "email": "alex@example.com"},
        )

        assert created_response.status_code == 201
        student = created_response.json()
        assert student == {
            "id": 1,
            "name": "Alex Morgan",
            "age": 20,
            "email": "alex@example.com",
        }

        list_response = client.get("/students")
        assert list_response.status_code == 200
        assert list_response.json() == [student]

        get_response = client.get(f"/students/{student['id']}")
        assert get_response.status_code == 200
        assert get_response.json() == student

        delete_response = client.delete(f"/students/{student['id']}")
        assert delete_response.status_code == 204
        assert delete_response.content == b""

        assert client.get("/students").json() == []
        assert client.get(f"/students/{student['id']}").status_code == 404


def test_create_student_defaults_optional_email_to_null(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        response = client.post("/students", json={"name": "Sam Lee", "age": 18})

    assert response.status_code == 201
    assert response.json()["email"] is None


def test_create_student_rejects_invalid_data(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        blank_name = client.post("/students", json={"name": "  ", "age": 18})
        invalid_age = client.post("/students", json={"name": "Sam Lee", "age": 0})
        invalid_email = client.post(
            "/students",
            json={"name": "Sam Lee", "age": 18, "email": "not-an-email"},
        )

    assert blank_name.status_code == 422
    assert invalid_age.status_code == 422
    assert invalid_email.status_code == 422


def test_delete_unknown_student_returns_not_found(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        response = client.delete("/students/999")

    assert response.status_code == 404

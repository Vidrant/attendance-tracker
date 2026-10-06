from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "OK"


def test_get_items():
    client = app.test_client()

    response = client.get("/items")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_item():
    client = app.test_client()

    record = {
        "student_id": 101,
        "student_name": "Rohit",
        "date": "2026-10-06",
        "status": "Present"
    }

    response = client.post("/items", json=record)

    assert response.status_code == 201
    assert response.get_json()["record"] == record

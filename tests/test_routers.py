from fastapi.testclient import TestClient

from src.stakefish_test.main import app

client = TestClient(app)


def test_validate_ok():
    response = client.post(
        "/tools/validate",
        json={"ip": "192.168.5.4"},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": True}


def test_validate_false():
    response = client.post(
        "/tools/validate",
        json={"ip": "292.168.5.4"},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_validate_error():
    response = client.post(
        "/tools/validate",
        json={"NONE": "292.168.5.4"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "ip"],
                "msg": "Field required",
                "input": {"NONE": "292.168.5.4"},
            }
        ]
    }

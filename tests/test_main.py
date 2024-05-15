import os
import time

from fastapi.testclient import TestClient

from src.stakefish_test.main import VERSION, app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "up",
    }


def test_root_no_k8s():
    response = client.get("/")
    assert response.status_code == 200

    mock_time = time.time()
    json_response = response.json()
    assert "date" in json_response
    json_response["date"] = mock_time
    assert json_response == {
        "version": VERSION,
        "date": mock_time,
        "kubernetes": False,
    }


def test_root_k8s():
    os.environ["KUBERNETES_SERVICE_HOST"] = "10.0.10.10"
    response = client.get("/")
    assert response.status_code == 200

    mock_time = time.time()
    json_response = response.json()
    assert "date" in json_response
    json_response["date"] = mock_time
    assert json_response == {
        "version": VERSION,
        "date": mock_time,
        "kubernetes": True,
    }

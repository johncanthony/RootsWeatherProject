from fastapi.testclient import TestClient
from ManagerAPI import managerAPI

client = TestClient(managerAPI)


def test_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"managerAPI": "up"}

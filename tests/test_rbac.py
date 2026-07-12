import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.security.permissions import require_roles
from app.auth.constants import UserRole
from fastapi import Depends

# Initialize FastAPI test client
client = TestClient(app)

# Register a temporary test route on the main app for authorization checking
@app.get("/test-rbac-guard")
def rbac_guard_endpoint(current_user = Depends(require_roles(UserRole.FLEET_MANAGER))):
    return {"success": True}

def test_rbac_flow():
    """
    Integration test validating RBAC controls:
    - Login as Fleet Manager (manager@example.com) -> Access granted (200 OK)
    - Login as Dispatcher (dispatcher@example.com) -> Access forbidden (403 Forbidden)
    - No authentication / Invalid token -> Access unauthorized (401 Unauthorized)
    """
    # 1. Test Login as Fleet Manager
    response = client.post("/auth/login", json={
        "email": "manager@example.com",
        "password": "Password123!"
    })
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    manager_token = res_data["data"]["access_token"]

    # 2. Test Login as Dispatcher
    response = client.post("/auth/login", json={
        "email": "dispatcher@example.com",
        "password": "Password123!"
    })
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    dispatcher_token = res_data["data"]["access_token"]

    # 3. Test Access /test-rbac-guard with Fleet Manager (should succeed)
    headers = {"Authorization": f"Bearer {manager_token}"}
    response = client.get("/test-rbac-guard", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # 4. Test Access /test-rbac-guard with Dispatcher (should be Forbidden)
    headers = {"Authorization": f"Bearer {dispatcher_token}"}
    response = client.get("/test-rbac-guard", headers=headers)
    assert response.status_code == 403
    res_json = response.json()
    assert res_json["success"] is False
    assert res_json["errorCode"] == "FORBIDDEN"

    # 5. Test Access /test-rbac-guard without Token (should be Unauthorized)
    response = client.get("/test-rbac-guard")
    assert response.status_code == 401
    res_json = response.json()
    assert res_json["success"] is False
    assert res_json["errorCode"] == "INVALID_TOKEN"

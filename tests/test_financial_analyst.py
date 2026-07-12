import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(email: str) -> str:
    response = client.post("/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    return res_data["data"]["access_token"]

@pytest.fixture(scope="module")
def analyst_token():
    return get_token("financial@example.com")

@pytest.fixture(scope="module")
def manager_token():
    return get_token("manager@example.com")

@pytest.fixture(scope="module")
def dispatcher_token():
    return get_token("dispatcher@example.com")

@pytest.fixture(scope="module")
def safety_token():
    return get_token("safety@example.com")


def test_rbac_denied_for_other_roles(manager_token, dispatcher_token, safety_token):
    """
    Ensures that other roles (Fleet Manager, Dispatcher, Safety Officer) are rejected with 403 Forbidden.
    """
    endpoints = [
        "/financial/dashboard",
        "/financial/analytics",
        "/financial/reports?report_type=fuel",
        "/financial/export/csv?report_type=fuel"
    ]

    for token in [manager_token, dispatcher_token, safety_token]:
        headers = {"Authorization": f"Bearer {token}"}
        for ep in endpoints:
            response = client.get(ep, headers=headers)
            assert response.status_code == 403
            res_json = response.json()
            assert res_json["success"] is False
            assert res_json["errorCode"] == "FORBIDDEN"


def test_dependency_error_for_financial_analyst(analyst_token):
    """
    Ensures that the Financial Analyst gets 503 Service Unavailable with a dependency missing message
    because Trip, FuelLog, Expense, and Maintenance tables are missing from the schema.
    """
    endpoints = [
        "/financial/dashboard",
        "/financial/analytics",
        "/financial/reports?report_type=fuel",
        "/financial/export/csv?report_type=fuel"
    ]

    headers = {"Authorization": f"Bearer {analyst_token}"}
    for ep in endpoints:
        response = client.get(ep, headers=headers)
        assert response.status_code == 503
        res_json = response.json()
        
        # Stream response has details under 'detail' key, standard APIResponse has under 'message'
        if "detail" in res_json:
            detail = res_json["detail"]
        elif "message" in res_json:
            detail = res_json["message"]
            assert res_json["success"] is False
            assert res_json["errorCode"] == "DEPENDENCY_MISSING"
        else:
            detail = ""
            
        assert "Dependency missing:" in detail

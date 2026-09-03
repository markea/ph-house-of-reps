import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Department, ServiceCatalog, Request, RequestApproval
from app.routers.auth import get_current_user
from app.database import get_db

@pytest.fixture
def override_auth_requester_maria(test_db):
    user = test_db.query(User).filter(User.email == "staff.maria@hrep.gov.ph").first()
    if not user:
        user = User(
            email="staff.maria@hrep.gov.ph",
            full_name="Maria Santos",
            role="Requester",
            position="Legislative Staff"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

    def _override():
        return user
    app.dependency_overrides[get_current_user] = _override
    yield user
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def override_auth_requester_juan(test_db):
    user = test_db.query(User).filter(User.email == "staff.juan@hrep.gov.ph").first()
    if not user:
        user = User(
            email="staff.juan@hrep.gov.ph",
            full_name="Juan Perez",
            role="Requester",
            position="Committee Staff"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

    def _override():
        return user
    app.dependency_overrides[get_current_user] = _override
    yield user
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def override_auth_approver(test_db):
    user = test_db.query(User).filter(User.role == "Approver").first()
    if not user:
        user = User(
            email="director.reyes@hrep.gov.ph",
            full_name="Atty. Roberto Reyes",
            role="Approver",
            position="Administrative Director"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

    def _override():
        return user
    app.dependency_overrides[get_current_user] = _override
    yield user
    app.dependency_overrides.pop(get_current_user, None)

def test_requester_cannot_approve_request(client, test_db, override_auth_requester_maria):
    # 1. Maria submits a request
    service = test_db.query(ServiceCatalog).first()
    res = client.post(
        "/api/requests/",
        json={
            "service_id": service.id,
            "priority": "Routine",
            "form_data": {"test": "data"}
        }
    )
    assert res.status_code == 200
    req_data = res.json()
    req_id = req_data["id"]
    assert "HREP-REQ-" in req_data["tracking_number"]

    # 2. Maria (Requester) tries to approve her own request -> Must be 403 Forbidden
    action_res = client.post(
        f"/api/requests/{req_id}/action",
        json={"action": "Approved", "remarks": "Self approval attempt"}
    )
    assert action_res.status_code == 403
    assert "Forbidden" in action_res.json()["detail"]

def test_requester_cannot_view_another_requester_ticket(client, test_db, override_auth_requester_maria, override_auth_requester_juan):
    # Setup Maria
    maria = test_db.query(User).filter(User.email == "staff.maria@hrep.gov.ph").first()
    juan = test_db.query(User).filter(User.email == "staff.juan@hrep.gov.ph").first()
    service = test_db.query(ServiceCatalog).first()

    # Create Maria's request directly
    app.dependency_overrides[get_current_user] = lambda: maria
    res = client.post(
        "/api/requests/",
        json={
            "service_id": service.id,
            "priority": "Routine",
            "form_data": {"secret": "maria_notes"}
        }
    )
    req_id = res.json()["id"]

    # Now switch persona to Juan
    app.dependency_overrides[get_current_user] = lambda: juan

    # Juan tries to access Maria's ticket -> 403 Forbidden
    detail_res = client.get(f"/api/requests/{req_id}")
    assert detail_res.status_code == 403
    assert "Forbidden" in detail_res.json()["detail"]

def test_approver_can_approve_ticket(client, test_db, override_auth_approver):
    req = test_db.query(Request).first()
    res = client.post(
        f"/api/requests/{req.id}/action",
        json={"action": "Approved", "remarks": "Authorized by Director Reyes"}
    )
    assert res.status_code == 200
    assert res.json()["new_status"] == "Approved"
    assert "SHA256-AUTHENTICATED" in res.json()["digital_stamp"]

def test_daily_sequential_tracking_numbers(client, test_db, override_auth_requester_maria):
    service = test_db.query(ServiceCatalog).first()
    r1 = client.post("/api/requests/", json={"service_id": service.id, "form_data": {}}).json()
    r2 = client.post("/api/requests/", json={"service_id": service.id, "form_data": {}}).json()
    
    t1 = r1["tracking_number"]
    t2 = r2["tracking_number"]
    
    seq1 = int(t1.split("-")[-1])
    seq2 = int(t2.split("-")[-1])
    assert seq2 == seq1 + 1


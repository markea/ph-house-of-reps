def test_health_and_ready_probes(client):
    # Liveness probe
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # Readiness probe
    res_ready = client.get("/readyz")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "ready"

def test_service_catalog_listing(client):
    res = client.get("/api/services/")
    assert res.status_code == 200
    services = res.json()
    assert len(services) >= 1
    assert services[0]["service_code"] == "MOTOR_POOL"

def test_request_lifecycle(client):
    # 1. Fetch service
    res_svc = client.get("/api/services/")
    service_id = res_svc.json()[0]["id"]

    # 2. Submit new request
    payload = {
        "service_id": service_id,
        "form_data": {"destination": "Senate of the Philippines", "passenger_count": 3},
        "priority": "Urgent"
    }
    res_create = client.post("/api/requests/", json=payload)
    assert res_create.status_code == 200
    created = res_create.json()
    assert created["tracking_number"].startswith("HREP-REQ-2026-")
    assert created["status"] == "Pending Approval"
    req_id = created["id"]

    # 3. Retrieve request detail
    res_detail = client.get(f"/api/requests/{req_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["tracking_number"] == created["tracking_number"]
    assert len(detail["audit_logs"]) >= 1

    # 4. Executive Approval Action
    res_appr = client.post(f"/api/requests/{req_id}/action", json={"action": "Approved", "remarks": "Approved by Director"})
    assert res_appr.status_code == 200
    assert res_appr.json()["new_status"] == "Approved"
    assert "SHA256-AUTHENTICATED" in res_appr.json()["digital_stamp"]

    # 5. CSAT Rating
    res_csat = client.post(f"/api/requests/{req_id}/csat", json={"rating": 5, "comment": "Excellent and prompt service!"})
    assert res_csat.status_code == 200
    assert res_csat.json()["status"] == "success"

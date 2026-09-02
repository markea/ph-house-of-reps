def test_adk_triage_motorpool(client):
    res = client.post("/api/agent/triage", json={"user_prompt": "I need a van for 5 passengers to the Senate tomorrow at 9am"})
    assert res.status_code == 200
    data = res.json()
    assert data["suggested_service_code"] == "MOTOR_POOL"
    assert data["confidence_score"] > 0.8
    assert data["extracted_fields"]["passenger_count"] == 5

def test_adk_triage_ac_repair(client):
    res = client.post("/api/agent/triage", json={"user_prompt": "Aircon in South Wing room 214 is leaking water onto desks"})
    assert res.status_code == 200
    data = res.json()
    assert data["suggested_service_code"] == "AC_REPAIR"
    assert "room 214" in data["extracted_fields"]["room_number"].lower()

def test_adk_triage_ict_support(client):
    res = client.post("/api/agent/triage", json={"user_prompt": "Need a high lumen projector and mic in Mitra hall for hearing"})
    assert res.status_code == 200
    data = res.json()
    assert data["suggested_service_code"] == "ICT_SUPPORT"

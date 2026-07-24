def test_health_and_docs_are_available(client):
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["message"].startswith("AI Service Desk")

import time


def test_profile_create_ticket(client):
    start = time.perf_counter()
    response = client.post(
        "/tickets",
        json={
            "title": "Profile test issue",
            "description": "This request is used to measure endpoint latency",
            "priority": "high",
        },
    )
    elapsed = time.perf_counter() - start

    assert response.status_code == 201
    assert elapsed < 2.0


def test_profile_list_tickets(client):
    start = time.perf_counter()
    response = client.get("/tickets")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 2.0


def test_profile_ai_summarize(client):
    start = time.perf_counter()
    response = client.post(
        "/ai/summarize",
        json={"ticket_description": "The login page is failing for many users after deployment and needs investigation."},
    )
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 2.0

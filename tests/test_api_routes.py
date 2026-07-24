from uuid import uuid4

from app.models.ticket import TicketPriority, TicketStatus


def test_create_ticket_route_returns_created_ticket(client):
    response = client.post(
        "/tickets",
        json={
            "title": "Login issue",
            "description": "User cannot sign in",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Login issue"
    assert payload["status"] == "open"


def test_get_ticket_route_returns_not_found_for_missing_ticket(client):
    response = client.get(f"/tickets/{uuid4()}")

    assert response.status_code == 404
    assert "was not found" in response.json()["detail"]


def test_ai_summarize_route_uses_fake_service(client):
    response = client.post(
        "/ai/summarize",
        json={"ticket_description": "The login page is failing for all users after deployment."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"].startswith("Support issue")
    assert "investigated" in payload["suggested_response"]

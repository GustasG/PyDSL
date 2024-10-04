from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to, has_entries

from tests.matchers import is_datetime, is_uuid


def test_valid_environment_creation(test_client: TestClient):
    response = test_client.post("/environment", json={"title": "First", "description": "First environment"})

    assert_that(response.status_code, equal_to(201))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("First"),
                "description": equal_to("First environment"),
                "created_at": is_datetime(),
                "updated_at": is_datetime(),
            }
        ),
    )


def test_invalid_environment_creation(test_client: TestClient):
    response = test_client.post(
        "/environment",
        json={
            "title": "a" * 512,
        },
    )

    assert_that(response.status_code, 422)


def test_valid_environment_retrieval(test_client: TestClient):
    response = test_client.post("/environment", json={"title": "First", "description": "First environment"})

    environment_id = response.json()["id"]
    response = test_client.get(f"/environment/{environment_id}")

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("First"),
                "description": equal_to("First environment"),
                "created_at": is_datetime(),
                "updated_at": is_datetime(),
            }
        ),
    )


def test_invalid_environment_retrieval(test_client: TestClient):
    response = test_client.get("/environment/00000000-0000-0000-0000-000000000000")

    assert_that(response.status_code, equal_to(404))
    assert_that(
        response.json(),
        has_entries({"detail": equal_to('Environment "00000000-0000-0000-0000-000000000000" not found')}),
    )

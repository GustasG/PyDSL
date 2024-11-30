from fastapi.testclient import TestClient
from freezegun import freeze_time
from hamcrest import assert_that, equal_to, has_entries, is_

from tests.matchers import is_uuid


@freeze_time("2000-01-01")
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
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2000-01-01T00:00:00"),
            }
        ),
    )


@freeze_time("2000-01-01")
def test_valid_environment_creation_without_arguments(test_client: TestClient):
    response = test_client.post("/environment", json={})

    assert_that(response.status_code, equal_to(201))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": is_(None),
                "description": is_(None),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2000-01-01T00:00:00"),
            }
        ),
    )


def test_invalid_environment_creation_with_too_long_title(test_client: TestClient):
    response = test_client.post(
        "/environment",
        json={
            "title": "a" * 512,
        },
    )

    assert_that(response.status_code, equal_to(422))


def test_invalid_environment_creation_with_too_long_description(test_client: TestClient):
    response = test_client.post(
        "/environment",
        json={
            "title": "First",
            "description": "a" * 2048,
        },
    )

    assert_that(response.status_code, equal_to(422))


@freeze_time("2000-01-01")
def test_valid_environment_retrieval(test_client: TestClient):
    response = test_client.post("/environment", json={"title": "foo", "description": "bar"})
    response.raise_for_status()
    environment = response.json()

    response = test_client.get(f"/environment/{environment['id']}")

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("foo"),
                "description": equal_to("bar"),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2000-01-01T00:00:00"),
            }
        ),
    )


def test_environment_retrieval_with_invalid_id(test_client: TestClient):
    response = test_client.get("/environment/00000000-0000-0000-0000-000000000000")

    assert_that(response.status_code, equal_to(404))
    assert_that(
        response.json(),
        has_entries({"detail": equal_to('Environment "00000000-0000-0000-0000-000000000000" not found')}),
    )


def test_environment_update_with_empty_payload(test_client: TestClient):
    with freeze_time("2000-01-01"):
        response = test_client.post("/environment", json={"title": "In test", "description": "Running test"})
        response.raise_for_status()
        environment = response.json()

    with freeze_time("2020-01-01"):
        response = test_client.patch(f"/environment/{environment['id']}", json={})

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("In test"),
                "description": equal_to("Running test"),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2020-01-01T00:00:00"),
            }
        ),
    )


def test_environment_update_with_only_title(test_client: TestClient):
    with freeze_time("2000-01-01"):
        response = test_client.post("/environment", json={"title": "Python", "description": "Programming language"})
        response.raise_for_status()
        environment = response.json()

    with freeze_time("2020-01-01"):
        response = test_client.patch(f"/environment/{environment['id']}", json={"title": "C++"})

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("C++"),
                "description": equal_to("Programming language"),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2020-01-01T00:00:00"),
            }
        ),
    )


def test_environment_update_with_only_description(test_client: TestClient):
    with freeze_time("2000-01-01"):
        response = test_client.post("/environment", json={"title": "Python", "description": "Programming language"})
        response.raise_for_status()
        environment = response.json()

    with freeze_time("2020-01-01"):
        response = test_client.patch(f"/environment/{environment['id']}", json={"description": "Scripting language"})

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("Python"),
                "description": equal_to("Scripting language"),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2020-01-01T00:00:00"),
            }
        ),
    )


def test_environment_update_with_both_title_and_description(test_client: TestClient):
    with freeze_time("2000-01-01"):
        response = test_client.post("/environment", json={"title": "C++", "description": "Scripting language"})
        response.raise_for_status()
        environment = response.json()

    with freeze_time("2020-01-01"):
        response = test_client.patch(
            f"/environment/{environment['id']}", json={"title": "C++", "description": "Programming language"}
        )

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "title": equal_to("C++"),
                "description": equal_to("Programming language"),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2020-01-01T00:00:00"),
            }
        ),
    )


def test_environment_update_with_invalid_id(test_client: TestClient):
    response = test_client.patch("/environment/00000000-0000-0000-0000-000000000000", json={"title": "Python"})

    assert_that(response.status_code, equal_to(404))
    assert_that(
        response.json(),
        has_entries({"detail": equal_to('Environment "00000000-0000-0000-0000-000000000000" not found')}),
    )


def test_environment_delete_with_invalid_id(test_client: TestClient):
    response = test_client.delete("/environment/00000000-0000-0000-0000-000000000000")

    assert_that(response.status_code, equal_to(404))
    assert_that(
        response.json(),
        has_entries({"detail": equal_to('Environment "00000000-0000-0000-0000-000000000000" not found')}),
    )


def test_environment_delete_with_valid_id(test_client: TestClient):
    response = test_client.post("/environment", json={"title": "Delete test"})
    response.raise_for_status()
    environment = response.json()

    response = test_client.delete(f"/environment/{environment['id']}")

    assert_that(response.status_code, equal_to(204))

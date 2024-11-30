from fastapi.testclient import TestClient
from freezegun import freeze_time
from hamcrest import assert_that, equal_to, has_entries

from tests.matchers import is_uuid

SAMPLE_ENVIRONMENT = {"title": "Testing", "description": "Testing environment for definitions"}

MUL_VALUES_CODE = """
def mul(a: int, b: int) -> int:
    return a * b
"""

SUM_VALUES_CODE = """
def sum(a: int, b: int) -> int:
    return a + b
"""


@freeze_time("2000-01-01")
def test_valid_definition_creation(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.post(f"/environment/{environment['id']}/definition", json={"code": MUL_VALUES_CODE})

    assert_that(response.status_code, equal_to(201))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": is_uuid(),
                "environment_id": equal_to(environment["id"]),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2000-01-01T00:00:00"),
                "code": equal_to(MUL_VALUES_CODE.strip()),
            }
        ),
    )


def test_valid_definition_creation_into_nonexistent_environment(test_client: TestClient):
    response = test_client.post(
        "/environment/00000000-0000-0000-0000-000000000000/definition", json={"code": MUL_VALUES_CODE}
    )

    assert_that(response.status_code, equal_to(404))


def test_reading_all_definitions_when_there_are_none(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.get(f"/environment/{environment['id']}/definition")

    assert_that(response.status_code, equal_to(200))
    assert_that(response.json(), equal_to([]))


@freeze_time("2000-01-01")
def test_valid_definition_retrieval(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.post(f"/environment/{environment['id']}/definition", json={"code": MUL_VALUES_CODE})
    response.raise_for_status()
    definition = response.json()

    response = test_client.get(f"/environment/{environment['id']}/definition/{definition['id']}")

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": equal_to(definition["id"]),
                "environment_id": equal_to(environment["id"]),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2000-01-01T00:00:00"),
                "code": equal_to(MUL_VALUES_CODE.strip()),
            }
        ),
    )


def test_invalid_definition_retrieval(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.get(f"/environment/{environment['id']}/definition/00000000-0000-0000-0000-000000000000")

    assert_that(response.status_code, equal_to(404))


def test_valid_environment_update_with_valid_payload(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    with freeze_time("2000-01-01"):
        response = test_client.post(f"/environment/{environment['id']}/definition", json={"code": MUL_VALUES_CODE})

    response.raise_for_status()
    old_definition = response.json()

    with freeze_time("2020-01-01"):
        response = test_client.patch(
            url=f"/environment/{environment['id']}/definition/{old_definition['id']}",
            json={"code": SUM_VALUES_CODE.strip()},
        )

    assert_that(response.status_code, equal_to(200))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": equal_to(old_definition["id"]),
                "environment_id": equal_to(environment["id"]),
                "created_at": equal_to("2000-01-01T00:00:00"),
                "updated_at": equal_to("2020-01-01T00:00:00"),
                "code": equal_to(SUM_VALUES_CODE.strip()),
            }
        ),
    )


def test_deleting_valid_definition(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.post(f"/environment/{environment['id']}/definition", json={"code": MUL_VALUES_CODE})
    response.raise_for_status()
    definition = response.json()

    response = test_client.delete(f"/environment/{environment['id']}/definition/{definition['id']}")

    assert_that(response.status_code, equal_to(204))


def test_deleting_invalid_definition(test_client: TestClient):
    response = test_client.post("/environment", json=SAMPLE_ENVIRONMENT)
    response.raise_for_status()
    environment = response.json()

    response = test_client.delete(f"/environment/{environment['id']}/definition/00000000-0000-0000-0000-000000000000")

    assert_that(response.status_code, equal_to(404))

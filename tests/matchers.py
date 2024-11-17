import uuid

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description


class IsUUID(BaseMatcher):
    def _matches(self, item):
        try:
            uuid.UUID(item)
            return True  # noqa: TRY300
        except (TypeError, AttributeError, ValueError):
            return False

    def describe_to(self, description: Description):
        description.append_text("a valid UUID")


def is_uuid():
    return IsUUID()

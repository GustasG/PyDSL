import datetime
import uuid

from hamcrest.core.base_matcher import BaseMatcher


class IsDateTime(BaseMatcher):
    def __init__(self):
        self.failure_reason = ""

    def _matches(self, item):
        try:
            datetime.datetime.fromisoformat(item)
            return True
        except (TypeError, ValueError) as e:
            self.failure_reason = str(e)
            return False

    def describe_to(self, description):
        description.append_text("a valid ISO 8601 formatted string")

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(self.failure_reason)


class IsUUID(BaseMatcher):
    def __init__(self):
        self.failure_reason = ""

    def _matches(self, item):
        try:
            uuid.UUID(item)
            return True
        except (TypeError, AttributeError, ValueError) as e:
            self.failure_reason = str(e)
            return False

    def describe_to(self, description):
        description.append_text("a valid UUID string")

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(self.failure_reason)


def is_datetime():
    return IsDateTime()


def is_uuid():
    return IsUUID()

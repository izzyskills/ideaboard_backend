from sqlalchemy.types import TypeDecorator, String
from datetime import datetime


class DateTimeString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.isoformat()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return datetime.fromisoformat(value)
        return value

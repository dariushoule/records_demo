"""Record data models module."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RecordFileType(Enum):
    """Supported file types for records."""

    COMMA_SEPARATED = "csv"
    PIPE_SEPARATED = "psv"
    SPACE_SEPARATED = "ssv"


RecordFileType.delimiters = {
    RecordFileType.COMMA_SEPARATED: ',',
    RecordFileType.PIPE_SEPARATED: '|',
    RecordFileType.SPACE_SEPARATED: ' '
}


@dataclass
class Record:
    """Record data model."""

    last_name: str
    first_name: str
    email: str
    date_of_birth: datetime
    favorite_color: str

    def __iter__(self):
        """Make records iterable, order is stable."""
        return iter(self.__dict__.values())

    def __len__(self):
        """Return the number of columns in a record."""
        return len(self.__dict__.values())

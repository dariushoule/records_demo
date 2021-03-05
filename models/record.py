"""Record data models module."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from dateutil.parser import parse


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
    favorite_color: str
    date_of_birth: datetime
    _date_of_birth: datetime = field(init=False, repr=False)

    @property
    def date_of_birth(self) -> str:
        """Return date in M/D/YYYY format."""
        return self._date_of_birth.strftime("%m/%d/%Y")

    @date_of_birth.setter
    def date_of_birth(self, date_str: str):
        self._date_of_birth = parse(date_str)

    def as_list(self):
        """Return a representation of a record as a list."""
        return [self.last_name, self.first_name, self.email, self.favorite_color, self.date_of_birth]

    def __iter__(self):
        """Make records iterable, order is stable."""
        return iter(self.as_list())

    def __getitem__(self, n: int):
        """Make records subscriptable, order is stable."""
        return self.as_list()[n]

    def __len__(self):
        """Return the number of columns in a record."""
        return len(self.as_list())

    def __str__(self):
        """Return a string representation of this record."""
        return str(self.as_list())

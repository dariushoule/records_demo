"""Record domain functionality."""
import csv
import logging
from typing import List, Optional

from models.record import Record, RecordFileType

from dateutil.parser import parse, ParserError

logger = logging.getLogger(__name__)


def read_records(files: List[str]) -> List[Record]:
    """Given a list of files, combines them and maps them to Record entries."""
    records = []
    for file in files:
        try:
            *_, extension = file.rpartition(".")
            fmt = RecordFileType(extension)
        except ValueError:
            logger.warning(f'{file} is an unsupported file format, it will be skipped')
            continue

        try:
            with open(file, 'r', newline='') as in_stream:
                records += [Record(*row) for row in csv.reader(in_stream, delimiter=RecordFileType.delimiters[fmt])]
        except (TypeError, UnicodeDecodeError, ParserError):
            logger.warning(f'{file} could not be parsed, it will be skipped')
            continue

    return records


def column_value_for_sort(record: Record, column_number: int):
    """Return the best representation of a Record's column for sorting."""
    if record[column_number] == record.date_of_birth:
        # birth dates should be sorted temporally vs alphabetically
        return parse(record[column_number])
    else:
        return record[column_number]


def sort_records(records: List[Record], sorts: List[str]) -> Optional[List[Record]]:
    """Sorts records and returns a new list."""
    sorted_records = records

    # Perform sorts from least priority to most priority
    if records and len(records) > 0 and sorts and len(sorts) > 0:
        reversed_sorts = sorts[:]  # Don't introduce unexpected side-effects by mutating input list of sorts
        reversed_sorts.reverse()

        for sort in reversed_sorts:
            bad_sort_error = f'Fatal error, {sort} is an invalid sort.'

            if sort.count(',') != 1:
                raise ValueError(bad_sort_error)

            col_number, direction = sort.split(',')
            if not col_number.isdigit() or direction.lower() not in ["asc", "desc"]:
                raise ValueError(bad_sort_error)

            col_number = int(col_number)
            direction = direction.lower()

            if col_number < 0 or col_number >= len(records[0]):
                raise ValueError(f'Fatal error, {col_number} is not an in-range column number.')

            sorted_records = sorted(sorted_records, key=lambda record: column_value_for_sort(record, col_number),
                                    reverse=True if direction == "desc" else False)
    return sorted_records

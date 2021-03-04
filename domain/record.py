"""Record domain functionality"""
import csv
import logging
from typing import List

from models.record import Record, RecordFileType

logger = logging.getLogger(__name__)


def read_records(files: List[str]) -> List[Record]:
    records = []
    for file in files:
        try:
            *_, extension = file.rpartition(".")
            fmt = RecordFileType(extension)
        except ValueError:
            logger.warning(f'{file} is an unsupported file format, it will be skipped')
            continue

        with open(file, 'r', newline='') as in_stream:
            records += csv.reader(in_stream, delimiter=RecordFileType.delimiters[fmt])

    return records


def sort_records(records: List[Record], sort_col: int):
    sorted(records, key=lambda record: record[sort_col])

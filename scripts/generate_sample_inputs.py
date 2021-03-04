"""Generates example test inputs in <project_root>/sample_inputs/"""
import argparse
import csv
from pathlib import Path
from typing import List

from faker import Faker

from models.record import Record, RecordFileType

OUTPUT_PATH = Path(__file__).parent.parent / 'sample_inputs'
MIN_SAMPLE_LENGTH = 1
MAX_SAMPLE_LENGTH = 1000


def write_example_input(records: List[Record], fmt: RecordFileType):
    delimiters = {
        RecordFileType.COMMA_SEPARATED: ',',
        RecordFileType.PIPE_SEPARATED: '|',
        RecordFileType.SPACE_SEPARATED: ' '
    }

    with (OUTPUT_PATH / f"example.{fmt.value}").open('w', newline='', ) as out_stream:
        writer = csv.writer(out_stream, delimiter=delimiters[fmt])
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser(description='Generate example test inputs in <project_root>/sample_inputs/')
    parser.add_argument('-n', type=int, default=100,
                        help=f'Number of records to generate in test files, {MIN_SAMPLE_LENGTH}-{MAX_SAMPLE_LENGTH}')
    args = parser.parse_args()

    if args.n < MIN_SAMPLE_LENGTH or args.n > MAX_SAMPLE_LENGTH:
        parser.print_help()
        return

    fake = Faker()
    records = [Record(
        fake.last_name(),
        fake.first_name(),
        fake.email(),
        fake.color_name(),
        fake.date_of_birth()) for _ in range(args.n)]

    for file_type in RecordFileType:
        write_example_input(records, file_type)


if __name__ == '__main__':
    main()

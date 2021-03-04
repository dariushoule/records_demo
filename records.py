"""Command line and REST interfaces for the application."""
import argparse
import csv
import logging
import sys

from fastapi import FastAPI

from domain.record import read_records, sort_records
from models.record import RecordFileType

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hey rest client, you are looking dandy today"}


def cli_entry():
    """Command line entrypoint for the application."""
    logging.basicConfig(format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    parser = argparse.ArgumentParser(description='Accepts an arbitrary number of record files and sorts them')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='Record files to be parsed, supports *.csv, *.psv, and *.ssv')
    parser.add_argument('-s', '--sort', nargs='*', metavar='SORT', type=str,
                        help='Zero-based sort column index and direction. '
                             'Specify column number and direction separated by a comma. '
                             '"ASC" represents ascending, "DESC" represents descending. '
                             'Sort priority reflects the order sorts are provided.')
    parser.add_argument('-f', '--format', metavar='FORMAT', default="csv",
                        choices=['csv', 'psv', 'ssv'],
                        help='Format to output records in, accepts csv, psv, and ssv')
    args = parser.parse_args()
    records = read_records(args.files)
    writer = csv.writer(sys.stdout, delimiter=RecordFileType.delimiters[RecordFileType(args.format)])
    sorted_records = sort_records(records, args.sort)
    writer.writerows(sorted_records)


if __name__ == '__main__':
    cli_entry()

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
    logging.basicConfig(format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    parser = argparse.ArgumentParser(description='Accepts an arbitrary number of record files and sorts them')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='Record files to be parsed, supports *.csv, *.psv, and *.ssv')
    parser.add_argument('-s', '--sort', metavar='SORT', type=int, default=0,
                        help='Zero based sort column index, defaulting to the first column')
    parser.add_argument('-f', '--format', metavar='FORMAT', default="csv",
                        choices=['csv', 'psv', 'ssv'],
                        help='Format to output records in, accepts csv, psv, and ssv')
    args = parser.parse_args()
    records = read_records(args.files)
    sort_records(records, args.sort)
    writer = csv.writer(sys.stdout, delimiter=RecordFileType.delimiters[RecordFileType(args.format)])
    writer.writerows(records)


if __name__ == '__main__':
    cli_entry()

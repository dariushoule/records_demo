"""Command line and REST interfaces for the application."""
import argparse
import csv
import logging
import sys
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.openapi.utils import get_openapi
from pydantic.main import BaseModel

from domain.record import read_records, sort_records
from models.record import RecordFileType, Record

# API ------------------------------------------------------------------------------------------------------------------


app = FastAPI()

# Holds records for the duration this API instance's lifetime
web_records = []


class CreateRecordRequestModel(BaseModel):
    """Pydantic request model for adding a Record."""

    record: str
    fmt: Optional[str] = "csv"


@app.post('/records',
          status_code=201,
          response_model=List[str],
          operation_id="create_record",
          summary="Create a record",
          description="Create a record and save in-memory for the lifetime of this API instance. "
                      "Provide last name, first name, email, color, and date of birth respectively. "
                      "Separate values using the separator specified in fmt. csv:, psv:|, ssv: .")
async def add_record(request: CreateRecordRequestModel) -> List[str]:
    """Handle adding a Record to Record storage."""
    if request.fmt not in ['csv', 'psv', 'ssv']:
        raise HTTPException(status_code=422, detail="unsupported record format")

    try:
        delimiter = RecordFileType.delimiters[RecordFileType(request.fmt)]
        web_records.append([Record(*row) for row in csv.reader([request.record], delimiter=delimiter)][0])
    except TypeError:
        raise HTTPException(status_code=422, detail="record syntax invalid, failed to parse")
    return web_records[-1].as_list()


@app.get('/records',
         response_model=List[List[str]],
         operation_id="get_records",
         summary="Retrieve all records with optional sort",
         description="Retrieve all records with optional sort. "
                     "Multiple sorts are supported with the first being highest priority. "
                     "Sorts are specified with the format [column number],[direction]. "
                     "Example: 0,DESC to sort last name.")
async def get_records(sort: List[str] = Query(None)) -> List[List[str]]:
    """Retrieve all records with given sorting rules."""
    try:
        sorted_records = sort_records(web_records, sort)
    except ValueError:
        raise HTTPException(status_code=400, detail="sort parameters are invalid")
    return [r.as_list() for r in sorted_records]


@app.get('/records/email',
         response_model=List[List[str]],
         operation_id="get_records_email_sort",
         summary="Retrieve all records with email sort ascending",
         description="Retrieve all records with email sort ascending.")
async def get_records_email_sort() -> List[List[str]]:
    """Retrieve all records with pre-selected email sort."""
    return await get_records(['2,ASC'])


@app.get('/records/birthdate',
         response_model=List[List[str]],
         operation_id="get_records_birthdate_sort",
         summary="Retrieve all records with birthdate sort ascending",
         description="Retrieve all records with birthdate sort ascending.")
async def get_records_birthdate_sort() -> List[List[str]]:
    """Retrieve all records with pre-selected birthdate sort."""
    return await get_records(['4,ASC'])


@app.get('/records/name',
         response_model=List[List[str]],
         operation_id="get_records_name_sort",
         summary="Retrieve all records with name sort ascending",
         description="Retrieve all records with name sort ascending. Name is computed as '[First] [Last]'")
async def get_records_name_sort() -> List[List[str]]:
    """Retrieve all records with pre-selected first + last name sort."""
    # Sort by the combination of first + last name
    sorted_records = sorted(web_records, key=lambda record: f'{record[1]} {record[0]}')
    return [r.as_list() for r in sorted_records]


def customize_openapi():
    """Customize the openapi dashboard and add a title / version."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Records Demo Application",
        version="1.0",
        description="Record Demo Application REST API Documentation",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = customize_openapi


# CLI ------------------------------------------------------------------------------------------------------------------


def process_records(files: List[str], sort: List[str], fmt: str, output_stream=sys.stdout):
    """Accept a list of record files and outputs them in the given format, optionally sorting."""
    records = read_records(files)
    writer = csv.writer(output_stream, delimiter=RecordFileType.delimiters[RecordFileType(fmt)])
    sorted_records = sort_records(records, sort)
    writer.writerows(sorted_records)


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
    process_records(args.files, args.sort, args.format)


if __name__ == '__main__':
    cli_entry()

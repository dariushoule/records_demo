"""CLI Tests."""
import io
import tempfile
from os import unlink
from pathlib import Path

import pytest

import records


def test_process_records_file():
    """Processes a single file sorting by lastname ascending. Outputs as comma separated values."""
    str_io = io.StringIO()
    records.process_records([str(Path(__file__).parent / 'data' / 'test.csv')], ['0,ASC'], 'csv', str_io)
    with open('expected/test_process_records_file', 'rb') as expected_stream:
        assert str_io.getvalue().encode("ascii") == expected_stream.read()


def test_process_records_files():
    """Processes multiple files sorting by lastname ascending. Outputs as comma separated values."""
    files = [
        str(Path(__file__).parent / 'data' / 'test.csv'),
        str(Path(__file__).parent / 'data' / 'test.psv')
    ]
    str_io = io.StringIO()
    records.process_records(files, ['0,ASC'], 'csv', str_io)
    with open('expected/test_process_records_files', 'rb') as expected_stream:
        assert str_io.getvalue().encode("ascii") == expected_stream.read()


def test_process_records_sort_lastname():
    """Processes a file and sorts by a last name descending. Outputs as pipe separated values."""
    str_io = io.StringIO()
    records.process_records([str(Path(__file__).parent / 'data' / 'test.ssv')], ['0,DESC'], 'psv', str_io)
    with open('expected/test_process_records_sort_lastname', 'rb') as expected_stream:
        assert str_io.getvalue().encode("ascii") == expected_stream.read()


def test_process_records_sort_lastname_date():
    """Processes a file and sorts by a last name descending and date ascending. Outputs as comma separated values."""
    str_io = io.StringIO()
    records.process_records([str(Path(__file__).parent / 'data' / 'test.ssv')], ['0,DESC', '4,ASC'], 'csv', str_io)
    with open('expected/test_process_records_sort_lastname_date', 'rb') as expected_stream:
        assert str_io.getvalue().encode("ascii") == expected_stream.read()


# Test inputs: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/
def test_process_records_fuzz():
    """Fuzz test CLI parser against a variety of potentially difficult to handle inputs."""
    str_io = io.StringIO()
    with open(Path(__file__).parent / 'data' / 'big-list-of-naughty-strings.txt', 'rb') as in_stream:
        blns = in_stream.readlines()
        blns = [s for s in blns if not s.startswith(b'#') and len(s) > 0]

    for s in blns:
        with tempfile.NamedTemporaryFile('wb', suffix=".ssv", delete=False) as tmp_file:
            tmp_file.truncate()
            tmp_file.seek(0)
            tmp_file.write(s)
        records.process_records([tmp_file.name], ['0,DESC', '4,ASC'], 'csv', str_io)
        unlink(tmp_file.name)


def test_process_records_nonexistent_file():
    """Test error handling on non-existent / inaccessible files."""
    with pytest.raises(FileNotFoundError):
        records.process_records(['non-existent.csv'], ['0,ASC'], 'csv')


def test_process_records_bad_sort():
    """Test error handling on bad sorts."""
    with pytest.raises(ValueError):
        records.process_records([str(Path(__file__).parent / 'data' / 'test.ssv')], ['0,ZESC', '4,ASC'], 'csv')


def test_process_records_bad_output_format():
    """Test error handling on bad output formats."""
    with pytest.raises(ValueError):
        records.process_records([str(Path(__file__).parent / 'data' / 'test.ssv')], ['0,DESC', '4,ASC'], 'tsv')

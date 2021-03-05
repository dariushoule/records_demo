"""API Tests."""
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import records

client = TestClient(records.app)


# Utility --------------------------------------------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture for setup and teardown."""
    records.app = FastAPI()
    records.web_records = []
    yield


# Tests ----------------------------------------------------------------------------------------------------------------

def test_read_records_empty():
    """Test a read of records with no stored data."""
    response = client.get('/records')
    assert response.status_code == 200
    assert response.json() == []


def test_read_records_sort_1col():
    """Test a read of records with a single column sort (ascending and descending)."""
    client.post('/records', json={'record': 'alast|first|email|pumice|3-3-3333', 'fmt': 'psv'})
    client.post('/records', json={'record': '$last first email pumice 3-3-3333', 'fmt': 'ssv'})
    client.post('/records', json={'record': 'Llast first email pumice 3-3-3333', 'fmt': 'ssv'})
    client.post('/records', json={'record': 'zlast first email pumice 3-3-3333', 'fmt': 'ssv'})

    response = client.get('/records', params={'sort': '0,DESC'})
    assert response.status_code == 200
    assert response.json() == [['zlast', 'first', 'email', 'pumice', '03/03/3333'],
                               ['alast', 'first', 'email', 'pumice', '03/03/3333'],
                               ['Llast', 'first', 'email', 'pumice', '03/03/3333'],
                               ['$last', 'first', 'email', 'pumice', '03/03/3333']]

    response = client.get('/records', params={'sort': '0,ASC'})
    assert response.status_code == 200
    assert response.json() == [['$last', 'first', 'email', 'pumice', '03/03/3333'],
                               ['Llast', 'first', 'email', 'pumice', '03/03/3333'],
                               ['alast', 'first', 'email', 'pumice', '03/03/3333'],
                               ['zlast', 'first', 'email', 'pumice', '03/03/3333']]


def test_read_records_sort_3col():
    """Test a read of records with a three column sort."""
    client.post('/records', json={'record': 'smith|first|email|pumice|3-3-2222', 'fmt': 'psv'})
    client.post('/records', json={'record': 'smith,first,email,pumice,3-3-3333', 'fmt': 'csv'})
    client.post('/records', json={'record': 'smith first zmail pumice 3-3-3333', 'fmt': 'ssv'})
    client.post('/records', json={'record': 'smuth first email pumice 3-3-3333', 'fmt': 'ssv'})

    response = client.get('/records?sort=0,ASC&sort=2,DESC&sort=4,ASC')
    assert response.status_code == 200
    assert response.json() == [['smith', 'first', 'zmail', 'pumice', '03/03/3333'],
                               ['smith', 'first', 'email', 'pumice', '03/03/2222'],
                               ['smith', 'first', 'email', 'pumice', '03/03/3333'],
                               ['smuth', 'first', 'email', 'pumice', '03/03/3333']]


def test_read_records_sort_email():
    """Test a read of records with the email sort."""
    client.post('/records', json={'record': 'smith|first|a@b.c|pumice|3-3-2222', 'fmt': 'psv'})
    client.post('/records', json={'record': 'smith,first,i@b.c,pumice,3-3-3333', 'fmt': 'csv'})
    client.post('/records', json={'record': 'smith first G@b.c pumice 3-3-3333', 'fmt': 'ssv'})

    response = client.get('/records/email')
    assert response.status_code == 200
    assert response.json() == [['smith', 'first', 'G@b.c', 'pumice', '03/03/3333'],
                               ['smith', 'first', 'a@b.c', 'pumice', '03/03/2222'],
                               ['smith', 'first', 'i@b.c', 'pumice', '03/03/3333']]


def test_read_records_sort_birthdate():
    """Test a read of records with the birthdate sort."""
    client.post('/records', json={'record': 'smith|first|a@b.c|pumice|1-3-3001', 'fmt': 'psv'})
    client.post('/records', json={'record': 'smith,first,i@b.c,pumice,3-9-2234', 'fmt': 'csv'})
    client.post('/records', json={'record': 'smith first G@b.c pumice 8-3-2323', 'fmt': 'ssv'})

    response = client.get('/records/birthdate')
    assert response.status_code == 200
    assert response.json() == [['smith', 'first', 'i@b.c', 'pumice', '03/09/2234'],
                               ['smith', 'first', 'G@b.c', 'pumice', '08/03/2323'],
                               ['smith', 'first', 'a@b.c', 'pumice', '01/03/3001']]


def test_read_records_sort_name():
    """Test a read of records with first + last name sort."""
    client.post('/records', json={'record': 'hanks|tom|a@b.c|pumice|1-3-3001', 'fmt': 'psv'})
    client.post('/records', json={'record': 'gomez,selena,i@b.c,pumice,3-9-2234', 'fmt': 'csv'})
    client.post('/records', json={'record': 'smith,selena,i@b.c,pumice,3-9-2234', 'fmt': 'csv'})
    client.post('/records', json={'record': 'pratt chris G@b.c pumice 8-3-2323', 'fmt': 'ssv'})

    response = client.get('/records/name')
    assert response.status_code == 200
    assert response.json() == [['pratt', 'chris', 'G@b.c', 'pumice', '08/03/2323'],
                               ['gomez', 'selena', 'i@b.c', 'pumice', '03/09/2234'],
                               ['smith', 'selena', 'i@b.c', 'pumice', '03/09/2234'],
                               ['hanks', 'tom', 'a@b.c', 'pumice', '01/03/3001']]


def test_add_record():
    """Test a basic persist of a record."""
    payload = {
        'record': 'lasty,mctesterson,l.mctesterson@nasa.gov,mahogany,"apr 2, 1991"',
        'fmt': 'csv'
    }

    response = client.post('/records', json=payload)
    assert response.status_code == 201
    assert response.json() == ['lasty', 'mctesterson', 'l.mctesterson@nasa.gov', 'mahogany', '04/02/1991']


def test_add_record_no_body():
    """Test persist error handling: no body."""
    response = client.post('/records')
    assert response.status_code == 422
    assert 'field required' in response.text


def test_add_record_missing_field():
    """Test persist error handling: bad record with missing favorite color value."""
    payload = {
        'record': 'lasty,mctesterson,l.mctesterson@nasa.gov,"apr 2, 1991"',
        'fmt': 'csv'
    }

    response = client.post('/records', json=payload)
    assert response.status_code == 422
    assert "record syntax invalid" in response.text


def test_add_record_bad_format():
    """Test persist error handling: bad format."""
    payload = {
        'record': 'lasty,mctesterson,l.mctesterson@nasa.gov,red,"apr 2, 1991"',
        'fmt': 'xml'
    }

    response = client.post('/records', json=payload)
    assert response.status_code == 422
    assert "unsupported record format" in response.text


# Test inputs: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/
def test_add_record_fuzz():
    """Fuzz test persist against a variety of potentially difficult to handle inputs."""
    with open(Path(__file__).parent / 'data' / 'big-list-of-naughty-strings.txt', 'rb') as in_stream:
        blns = in_stream.readlines()
        blns = [s for s in blns if not s.startswith(b'#') and len(s) > 0]

    # Fuzz test: a record column
    for s in blns:
        payload = b'{"record":"a,b,c,d,' + s + b'","fmt":"csv"}'
        response = client.post('/records', data=payload)
        assert response.status_code == 422

    # Fuzz test: record
    for s in blns:
        payload = b'{"record":"' + s + b'","fmt":"csv"}'
        response = client.post('/records', data=payload)
        assert response.status_code == 422

    # Fuzz test: fmt
    for s in blns:
        payload = b'{"record":"a,b,c,d,1-1-1900","fmt":"' + s + b'"}'
        response = client.post('/records', data=payload)
        assert response.status_code == 422

    # Fuzz test: payload
    for s in blns:
        response = client.post('/records', data=s)
        assert response.status_code == 422

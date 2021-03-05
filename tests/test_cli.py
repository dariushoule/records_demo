import pytest

import records


def test_process_records_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        records.process_records(['non-existent.csv'], ['0,ASC'], 'csv')

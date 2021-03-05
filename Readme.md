Records Demo Application
------------------------

_Records Demo_ is a small CLI / HTTP based application that demonstrates:
- File input and transformation
- Basic HTTP/REST concepts

### Setup

Application requires Python >=3.9 and [pipenv](https://pipenv.pypa.io/en/latest/)

#### Install Dependencies
```
pipenv install
```

### Usage

#### From the command line
```
pipenv run python records.py
```

#### Command line examples
```
# Read sample inputs and sort by email descending, then last name ascending
pipenv run python records.py sample_inputs/example.csv -s 2,DESC 0,ASC

# Read sample inputs and sort by birth date ascending
pipenv run python records.py sample_inputs/example.csv -s 4,ASC

# Read sample inputs and sort by last name descending
pipenv run python records.py sample_inputs/example.csv -s 0,DESC

# Combining multiple files into a single set of pipe separated values
pipenv run python records.py sample_inputs/example.csv sample_inputs/example.psv sample_inputs/example.ssv -f psv
```

#### As a REST API
```
pipenv run uvicorn records:app
```

See the interactive openAPI dashboard at [http://localhost:8000/docs](http://localhost:8000/docs)
for usage and testing assistance.

#### Generating sample inputs to test with
```
pipenv run python scripts/generate_sample_inputs.py
```

### Linting

From the project root:
```
flake8
```

### Unit Testing
```
pytest records_demo
```